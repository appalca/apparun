"""
This module contains all the functions and classes used to manipulate the expressions
for the parameters of an impact model.
"""
from __future__ import annotations

import math
import re
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, List, Self, Union

if TYPE_CHECKING:
    from apparun.parameters import ImpactModelParams

import networkx as nx
import numpy
import sympy
from pydantic import BaseModel, ValidationError, field_validator, model_validator
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import ValidationInfo
from sympy import Expr, sympify

from apparun.exceptions import InvalidExpr


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
    expression are only functions of the modules math and numpy.

    :param expr: an expression.
    :returns: True if the expression is a valid arithmetic expression, else False.
    """
    tokens_patterns = {
        "FUN_ID": r"\w+\b(?=\()",
        "ID": r"[a-zA-Z_]+",
        "NUMBER": r"\-?\d+(\.\d+(e\-?\d+)?)?",
        "L_PAREN": r"\(",
        "R_PAREN": r"\)",
        "OP": r"\+|\-|\*{1,2}|/{1,2}|%",
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
    allowed_funcs = dir(math) + dir(numpy)
    return valid and nb_paren == 0 and all(fun in allowed_funcs for fun in fun_names)


class ParamsValuesSet(BaseModel):
    """
    Represents a set of expressions for a set of parameters of an impact model.
    Each expression in the set is associated to one and only one parameter.
    """

    expressions: Dict[str, ParamExpr]

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
        return ParamsValuesSet(**{"expressions": parsed_expressions})

    @property
    def dependencies_graph(self) -> nx.DiGraph:
        """
        Build the dependencies graph of the expressions.

        :returns: an oriented graph representing the dependencies between the expressions.
        """
        return nx.DiGraph(
            [
                (name, dep)
                for name, expr in self.expressions.items()
                for dep in expr.dependencies
            ]
        )

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
        invalid_deps = sorted(set(self.dependencies) - set(parameters.names))
        if invalid_deps:
            raise PydanticCustomError(
                "no_such_param",
                "No such parameters: {invalid_parameters}",
                {"invalid_parameters": tuple(invalid_deps)},
            )
        # Check all the dependencies are float type parameters
        non_float_deps = sorted(
            [
                dep
                for dep in self.dependencies
                if dep not in parameters[dep].type != "float"
            ]
        )
        if non_float_deps:
            raise PydanticCustomError(
                "dependencies_type",
                "Invalid type for the dependencies {invalid_parameters}, expected type {required_type}",
                {
                    "invalid_parameters": tuple(non_float_deps),
                    "required_type": "float",
                },
            )
        return self

    @property
    def dependencies(self) -> List[str]:
        return re.findall(r"[a-zA-Z_]+\b(?!\()", self.expr)

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
