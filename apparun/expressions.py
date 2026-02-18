"""
This module contains all the functions and classes used to manipulate the expressions
for the parameters of an impact model.
"""
from __future__ import annotations

import math
import re
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Any, Dict, List, Self, Union

import networkx as nx
import numpy
import sympy
from pydantic import BaseModel, ValidationError, field_validator, model_validator
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import ValidationInfo
from sympy import Expr, sympify

from apparun.exceptions import InvalidExpr
from apparun.logger import logger
from apparun.parameters import ImpactModelParams


def parse_expr(expr: Any) -> Expr:
    """
    Parses an arithmetic expression using sympy.
    Raises an error if the expression is invalid.

    :param expr: an expression.
    :returns: a sympy expression object.
    """
    if isinstance(expr, str):
        if validate_expr(expr):
            return sympy.parse_expr(expr)
    raise InvalidExpr("invalid_expr", expr)


def validate_expr(expr: str) -> bool:
    """
    Check if an expression is a valid arithmetic expression that
    can be used in an impact model. Allowed functions inside an
    expression are only functions of the modules math, numpy and sympy.

    :param expr: an expression.
    :returns: True if the expression is a valid arithmetic expression, else False.
    """
    tokens_patterns = {
        "FUN_ID": r"\w+\b(?=\()",
        "ID": r"[a-zA-Z_]+",
        "NUMBER": r"\-?\d+(\.\d+(e\-?\d+)?)?",
        "L_PAREN": r"\(",
        "R_PAREN": r"\)",
        "OP": r"\+|\-|\*{1,2}|/{1,2}|%|/|<=?|>=?|={2}",
        "COMMA": r",",
        "WS": r"\s+",
    }

    tokens_predecessors = {
        "ID": ["OP", "L_PAREN", "COMMA"],
        "FUN_ID": ["OP", "L_PAREN", "COMMA"],
        "NUMBER": ["OP", "L_PAREN", "COMMA"],
        "L_PAREN": ["OP", "ID", "L_PAREN", "COMMA", "FUN_ID"],
        "R_PAREN": ["NUMBER", "ID", "R_PAREN"],
        "COMMA": ["NUMBER", "ID", "R_PAREN"],
        "OP": ["NUMBER", "ID", "R_PAREN"],
    }

    expr_copy = str(expr)
    valid = True
    previous_token = None
    nb_paren = 0
    while valid and len(expr_copy) > 0:
        for token, pattern in tokens_patterns.items():
            match = re.match(pattern, expr_copy)
            if bool(match):
                expr_copy = expr_copy[match.span()[1] :]
                if token == "WS":
                    break
                elif token == "L_PAREN":
                    nb_paren += 1
                elif token == "R_PAREN":
                    nb_paren -= 1
                if (
                    previous_token is not None
                    and previous_token not in tokens_predecessors[token]
                ):
                    valid = False
                else:
                    previous_token = token
                break
        else:
            valid = False

    fun_names = re.findall(tokens_patterns["FUN_ID"], expr)
    allowed_funcs = dir(math) + dir(numpy) + dir(sympy)
    return valid and nb_paren == 0 and all(fun in allowed_funcs for fun in fun_names)


class ParamsValuesSet(BaseModel):
    """
    Represents a set of expressions for a set of parameters of an impact model.
    Each expression in the set is associated to one and only one parameter.
    """

    expressions: Dict[str, ParamExpr]
    parameters: ImpactModelParams

    def __getitem__(self, item):
        if item not in self.expressions:
            raise KeyError()
        return self.expressions[item]

    @classmethod
    def build(
        cls,
        expressions: Dict[str, Union[float, int, str, dict]],
        parameters: ImpactModelParams,
    ) -> ParamsValuesSet:
        """
        Builder function to create instance of this class.

        :param expressions: a set of expressions, each expression is associated to one parameter.
        :param parameters: parameters associated to the expressions.
        :returns: an instance of this class with the given expressions.
        """
        errors = []
        # Parsing the expressions
        parsed_expressions = {}
        for name, expr in expressions.items():
            try:
                parsed_expressions[name] = ParamExpr.parse(expr, name, parameters)
            except ValidationError as e:
                for err in e.errors():
                    errors.append(
                        {
                            "type": PydanticCustomError(
                                err["type"],
                                "Invalid expression "
                                + str(expr)
                                + " for the parameter {target_parameter}: "
                                + err["msg"][0].lower()
                                + err["msg"][1:],
                                (err["ctx"] if "ctx" in err else {})
                                | {"target_parameter": name},
                            ),
                            "loc": err["loc"],
                            "msg": "",
                            "input": expr,
                        }
                    )
        if errors:
            raise ValidationError.from_exception_data("", line_errors=errors)
        return ParamsValuesSet(
            **{"expressions": parsed_expressions, "parameters": parameters}
        )

    @property
    def dependencies_graph(self) -> nx.DiGraph:
        """
        Build the dependencies graph of the expressions.

        :returns: an oriented graph representing the dependencies between the expressions.
        """
        graph_nodes = [
            (name, dep)
            for name, expr in self.expressions.items()
            for dep in expr.dependencies
        ]
        graph_nodes = [
            (
                self.parameters.find_corresponding_parameter(
                    param[0], must_find_one=True
                ).name,
                self.parameters.find_corresponding_parameter(
                    param[1], must_find_one=True
                ).name,
            )
            for param in graph_nodes
        ]
        return nx.DiGraph(graph_nodes)

    def dependencies_cycle(self) -> List[str]:
        """
        Detect if there is a dependencies cycle between the expressions.

        :returns: the list of the parameters whose expressions are creating a dependencies cycle
        or an empty list if there is no cycle.
        """
        try:
            return [edge[0] for edge in nx.find_cycle(self.dependencies_graph)]
        except nx.NetworkXNoCycle:
            return []

    def evaluate(self) -> Dict[str, Union[float, int, str]]:
        """
        Evaluate the value of each expression, there must be no dependency cycle
        in the set. If there is a dependency cycle, a ValueError is raised.

        :returns: the value of each expression, the keys are the name of the parameter associated to the expression.
        """
        if self.dependencies_cycle():
            raise ValueError(
                "Impossible to evaluate the expressions since there is a dependency cycle between them"
            )

        order = list(nx.topological_sort(self.dependencies_graph))
        order += [name for name in self.expressions.keys() if name not in order]

        values = {}
        for name in reversed(order):
            deps_values = {
                param_name: value
                for param_name, value in values.items()
                if param_name in self.expressions[name].dependencies
            }

            values[name] = self.expressions[name].evaluate(deps_values)
            if self.parameters[name].type == "enum":
                oh_values = self.parameters[name].transform(values[name])
                for enum_option, oh_value in oh_values.items():
                    values[enum_option] = oh_value
        return values


class ParamExpr(BaseModel, ABC):
    """
    Base class for the expressions used as values for the parameters of
    an impact model.
    """

    @classmethod
    def parse(
        cls,
        raw_expr: Union[float, int, str, dict],
        param: str,
        parameters: ImpactModelParams,
    ) -> ParamExpr:
        """
        Parse an expression.

        :param raw_expr: the expression to parse.
        :param param: name of the parameter associated to this expression.
        :param parameters: information about the parameters of the impact model.

        :returns: the parsed expression.
        """
        match raw_expr:
            case dict():
                return ParamEnumExpr.model_validate(
                    {"expr": raw_expr},
                    context={"param": param, "parameters": parameters},
                )
            case str() if parameters[param].type == "enum":
                return ParamEnumConst(**{"value": raw_expr})
            case str() if parameters[param].type == "float":
                return ParamFloatExpr.model_validate(
                    {"expr": raw_expr}, context={"parameters": parameters}
                )
            case _:
                return ParamFloatConst(**{"value": raw_expr})

    @property
    def dependencies(self) -> List[str]:
        """
        :returns: the list of the parameters whose are the dependencies of this expression.
        """
        return []

    @property
    @abstractmethod
    def is_complex(self) -> bool:
        """
        :returns: True if the expression is a complex one, else False.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def raw_version(self):
        """
        :returns: the raw version of the expression.
        """
        raise NotImplementedError()

    @abstractmethod
    def evaluate(
        self, dependencies_values: Dict[str, Union[float, int, str]]
    ) -> Union[float, int, str]:
        """
        Evaluate this expression based on the values of its dependencies.

        :param dependencies_values: the values of the dependencies of this expression.
        :returns: the evaluated value for this expression.
        """
        raise NotImplementedError()


class ParamFloatConst(ParamExpr):
    """
    Represents a float type constant.
    """

    value: float

    @property
    def is_complex(self) -> bool:
        return False

    @property
    def raw_version(self):
        return self.value

    def evaluate(
        self, dependencies_values: Dict[str, Union[float, int, str]]
    ) -> Union[float, int, str]:
        return self.value


class ParamEnumConst(ParamExpr):
    """
    Represents an constant enum type.
    """

    value: str

    @property
    def is_complex(self) -> bool:
        return False

    @property
    def raw_version(self):
        return self.value

    def evaluate(
        self, dependencies_values: Dict[str, Union[float, int, str]]
    ) -> Union[float, int, str]:
        return self.value


class ParamFloatExpr(ParamExpr):
    """
    Represents a float type expression.
    """

    expr: str

    @field_validator("expr", mode="before")
    @classmethod
    def validate_expr(cls, expr: str) -> str:
        """
        Check that the expression is a valid float expression.

        :parameter expr: the expression to validate.
        """
        if not validate_expr(expr):
            raise PydanticCustomError("float_expr", "Invalid float expression")
        return expr

    @model_validator(mode="after")
    def validate_dependencies(self, info: ValidationInfo) -> Self:
        """
        Check all the dependencies of the expression are
        existing parameters of the impact model and are of type float.

        :parameter info: useful information used for validating data.
        """
        parameters = info.context["parameters"]
        # Check all the dependencies are parameters of the impact model
        for dep in self.dependencies:
            try:
                parameters.find_corresponding_parameter(dep, must_find_one=True)
            except ValueError:
                raise PydanticCustomError(
                    "no_such_param",
                    "No such parameter: {invalid_parameters}",
                    {"invalid_parameter": dep},
                )
            if dep in [param.name for param in parameters if param.type == "enum"]:
                raise PydanticCustomError(
                    "dependencies_type",
                    "Invalid type for the dependency {invalid_parameter}, expected type {required_type}",
                    {
                        "invalid_parameter": dep,
                        "required_type": "float or dummy",
                    },
                )
        return self

    @property
    def dependencies(self) -> List[str]:
        return [str(symbol) for symbol in parse_expr(self.expr).free_symbols]

    @property
    def is_complex(self) -> bool:
        return True

    @property
    def raw_version(self):
        return self.expr

    def evaluate(
        self, dependencies_values: Dict[str, Union[float, int, str]]
    ) -> Union[float, int, str]:
        return sympify(self.expr).evalf(subs=dependencies_values)


class ParamEnumExpr(ParamExpr):
    """
    Represents an enum type expression.
    """

    param: str
    options: Dict[str, ParamExpr]

    @model_validator(mode="before")
    @classmethod
    def parse_sub_exprs(cls, data: Any, info: ValidationInfo) -> Any:
        """
        Validator use to parse the sub expressions.
        """
        data["options"] = {
            option: ParamExpr.parse(
                sub_expr, info.context["param"], info.context["parameters"]
            )
            for option, sub_expr in data["options"].items()
        }
        return data

    @model_validator(mode="before")
    @classmethod
    def validate_options(cls, data: Any, info: ValidationInfo) -> Any:
        """
        Check the expression contains all the options of the parameter used in it
        with no extra options. Also check that each option has an associated sub expression.
        """
        parameters = info.context["parameters"]
        param = data["param"]
        options = list(data["options"].keys())

        missing_options = sorted(set(parameters[param].options) - set(options))
        if missing_options:
            raise PydanticCustomError(
                "enum_expr_options",
                "Missing options {missing_options}",
                {"missing_options": tuple(missing_options), "extra_options": ()},
            )

        extra_options = sorted(set(options) - set(parameters[param].options))
        if extra_options:
            raise PydanticCustomError(
                "enum_expr_options",
                "The options {extra_options} are extra options and are not allowed",
                {"missing_options": (), "extra_options": tuple(extra_options)},
            )

        none_options = sorted(
            [option for option, sub_expr in data["options"].items() if sub_expr is None]
        )
        if none_options:
            raise PydanticCustomError(
                "enum_expr_empty_options",
                "The options {invalid_options} don't have associated sub expressions",
                {"invalid_options": tuple(none_options)},
            )

        return data

    @model_validator(mode="before")
    @classmethod
    def validate_param(cls, data: Any, info: ValidationInfo) -> Any:
        """
        Check the parameter used in the expression is an existing
        parameter of the impact model and that is an enum type parameter.
        """
        expr = data["expr"]

        dependencies = list(expr.keys())
        if len(dependencies) != 1:
            raise PydanticCustomError(
                "too_much_dependencies",
                "Required {required} dependencies, got {value}",
                {"required": 1, "value": len(dependencies)},
            )

        dependency = dependencies[0]
        parameters = info.context["parameters"]

        if dependency not in parameters.names:
            raise PydanticCustomError(
                "no_such_param",
                "The parameters {invalid_parameters} are not existing parameters",
                {"invalid_parameters": (dependency,)},
            )

        if parameters[dependency].type != "enum":
            raise PydanticCustomError(
                "dependencies_type",
                "Invalid type for the dependencies {invalid_parameters}, expected type {required_type}",
                {"invalid_parameters": (dependency,), "required_type": "enum"},
            )

        return {"param": dependency, "options": expr[dependency]}

    @property
    def dependencies(self) -> List[str]:
        deps = {self.param}
        for sub_expr in self.options.values():
            deps = deps | set(sub_expr.dependencies)
        return deps

    @property
    def is_complex(self) -> bool:
        return True

    @property
    def raw_version(self):
        return {
            self.param: {
                option: sub_expr.raw_version
                for option, sub_expr in self.options.items()
            }
        }

    def evaluate(
        self, dependencies_values: Dict[str, Union[float, int, str]]
    ) -> Union[float, int, str]:
        return self.options[dependencies_values[self.param]].evaluate(
            dependencies_values
        )


class ImpactModelParamsValues(BaseModel):
    """
    A set of values for the parameters of an impact model.

    ATTENTION!! Use the method from dict to build instance of this class.
    """

    values: Dict[str, List[Union[float, int, str]]]

    def __getitem__(self, item):
        if item in self.values.keys():
            return self.values[item]
        else:
            raise KeyError()

    @classmethod
    def from_dict(
        cls,
        parameters: ImpactModelParams,
        values: Dict[
            str, Union[float, int, str, dict, List[Union[float, int, str, dict]]]
        ],
    ) -> ImpactModelParamsValues:
        # Values with the default values for the parameters not in the values
        all_values = {
            **values,
            **{
                param.name: param.default
                for param in parameters
                if param.name not in values
            },
        }
        # Step 1 - Transform all values into lists
        empty_list_values = [
            name
            for name, value in values.items()
            if isinstance(value, list) and len(value) == 0
        ]
        if empty_list_values:
            raise ValidationError.from_exception_data(
                "",
                line_errors=[
                    {
                        "loc": ("values",),
                        "msg": "",
                        "type": PydanticCustomError(
                            "empty_list",
                            "The value for the parameter {parameter} can't be an empty list",
                            {"parameter": name},
                        ),
                    }
                    for name in empty_list_values
                ],
            )

        list_values = [value for value in values.values() if isinstance(value, list)]
        if any(
            len(list_values[0]) != len(list_values[i])
            for i in range(1, len(list_values))
        ):
            raise ValidationError.from_exception_data(
                "",
                line_errors=[
                    {
                        "loc": ("values",),
                        "msg": "",
                        "type": PydanticCustomError(
                            "lists_size_match", "List values must have matching sizes"
                        ),
                    }
                ],
            )

        size = max(map(len, list_values)) if list_values else 1
        list_values = {
            name: value if isinstance(value, list) else [value] * size
            for name, value in all_values.items()
        }

        # Step 2 - Transform the values to expressions
        exprs_sets = []
        for idx in range(size):
            exprs_sets.append(
                ParamsValuesSet.build(
                    {name: value[idx] for name, value in list_values.items()},
                    parameters,
                )
            )

        # Step 3 - Dependencies cycles detection
        for exprs_set in exprs_sets:
            try:
                cycle = exprs_set.dependencies_cycle()
                if cycle:
                    raise ValidationError.from_exception_data(
                        "",
                        line_errors=[
                            {
                                "loc": ("values",),
                                "msg": "",
                                "type": PydanticCustomError(
                                    "dependencies_cycle",
                                    "The expressions for the parameters {parameters} are inter-dependent",
                                    {"parameters": tuple(sorted(cycle))},
                                ),
                            }
                        ],
                    )
            except nx.NetworkXNoCycle:
                pass

        # Step 4 - Expressions' evaluation
        final_values = defaultdict(list)
        for exprs_set in exprs_sets:
            evals = exprs_set.evaluate()
            for name, value in evals.items():
                # Remove any dummy, if any
                if name in parameters.names:
                    final_values[name].append(value)

        # Step 5 - Validation of the final values
        errors = []
        for name, value in final_values.items():
            for idx, elem in enumerate(value):
                parameter = parameters[name]
                match parameter.type:
                    case "float":
                        if parameter.min is None or parameter.max is None:
                            logger.warning(
                                f"Parameter {parameter.name} does not have valid bounds. "
                                f"Consider calling update_bounds()."
                            )
                        elif elem < parameter.min or elem > parameter.max:
                            if exprs_sets[idx][name].is_complex:
                                logger.warning(
                                    "The value %s (got after evaluating the expression %s) for the parameter %s is outside its [min, max] range",
                                    str(elem),
                                    name,
                                    str(exprs_sets[idx][name].raw_version),
                                )
                            else:
                                logger.warning(
                                    "The value %s for the parameter %s is outside its [min, max] range",
                                    str(elem),
                                    name,
                                )
                    case "enum" if elem not in parameter.options:
                        if exprs_sets[idx][name].is_complex:
                            errors.append(
                                {
                                    "type": PydanticCustomError(
                                        "value_error",
                                        "Invalid value {value}, got after evaluating the expression {expr}, for the parameter {target_parameter}",
                                        {
                                            "value": elem,
                                            "target_parameter": name,
                                            "expr": str(
                                                exprs_sets[idx][name].raw_version
                                            ),
                                        },
                                    )
                                }
                            )
                        else:
                            errors.append(
                                {
                                    "type": PydanticCustomError(
                                        "value_error",
                                        "Invalid value {value} for the parameter {target_parameter}",
                                        {"value": elem, "target_parameter": name},
                                    )
                                }
                            )
        if errors:
            raise ValidationError.from_exception_data("", line_errors=errors)

        return ImpactModelParamsValues(**{"values": final_values})

    def items(self):
        return self.values.items()
