"""
This module contains all the functions and classes used to manipulate the expressions
for the parameters of an impact model.
"""
from __future__ import annotations

import math
import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

import networkx as nx
import numpy
import sympy
from pydantic import BaseModel, ValidationError
from pydantic_core import PydanticCustomError
from sympy import Expr, sympify

from apparun.exceptions import InvalidExpr


def parse_expr(expr: Any) -> Expr:
    """
    Parsed an arithmetic expression using sympy.
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
    can be used in an impact model.

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


class ImpactModelExprSet(BaseModel):
    """
    Represents a set of expressions for a set of parameters of an impact model.
    """

    expressions: Dict[str, ImpactModelExpr]
    _dependencies_graph: nx.DiGraph = None

    def __getitem__(self, item):
        if item not in self.expressions:
            raise KeyError()
        return self.expressions[item]

    @classmethod
    def build(
        cls,
        expressions: Dict[str, Union[float, int, str, dict]],
        params_infos: Dict[str, dict],
    ) -> ImpactModelExprSet:
        """
        Builder function to create instance of this class.

        :param expressions: a set of expressions, each expression is associated to one parameter.
        :param params_infos: information about the parameters, such as their type.
        :returns: an instance of this class with the given expressions.
        """
        errors = []
        # Parsing the expressions
        parsed_expressions = {}
        for name, expr in expressions.items():
            try:
                parsed_expressions[name] = ImpactModelExpr.parse(
                    expr, name, params_infos
                )
            except InvalidExpr as e:
                errors.append(
                    {
                        "type": PydanticCustomError(
                            e.type, "", {"target_parameter": name} | e.ctx
                        ),
                        "loc": (),
                        "msg": "",
                        "input": e.expr,
                    }
                )
        if errors:
            raise ValidationError.from_exception_data("", line_errors=errors)
        return ImpactModelExprSet(**{"expressions": parsed_expressions})

    @property
    def dependencies_graph(self) -> nx.DiGraph:
        """
        Build the dependencies graph of the expressions.

        :returns: an oriented graph.
        """
        if self._dependencies_graph is None:
            self._dependencies_graph = nx.DiGraph(
                [
                    (name, dep)
                    for name, expr in self.expressions.items()
                    for dep in expr.dependencies
                ]
            )
        return self._dependencies_graph

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

    def eval(self) -> Dict[str, Union[float, int, str]]:
        """
        Evaluate each expression, don't use this method is the method
        dependencies_cycle doesn't return an empty list.

        :returns: the value of each expression, the keys are the name of the parameter associated to the expression.
        """
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


class ImpactModelExpr(BaseModel, ABC):
    """
    Base class for the expressions used as values for the parameters of
    an impact model.
    """

    @classmethod
    def parse(
        cls,
        raw_expr: Union[float, int, str, dict],
        param: str,
        params_infos: Dict[str, dict],
    ) -> ImpactModelExpr:
        """
        Parse an expression.

        :param raw_expr: the expression to parse.
        :param param: name of the parameter associated to this expression.
        :param params_infos: information about the parameters of the impact model.

        :returns: the parsed expression.
        """
        match raw_expr:
            case dict():
                return ImpactModelEnumExpr.parse(raw_expr, param, params_infos)
            case str() if params_infos[param]["type"] == "enum":
                return ImpactModelEnumConst(**{"value": raw_expr})
            case str() if params_infos[param]["type"] == "float":
                return ImpactModelFloatExpr.parse(raw_expr, param, params_infos)
            case _:
                return ImpactModelFloatConst(**{"value": raw_expr})

    @property
    def dependencies(self) -> List[str]:
        """
        :returns: the list of the parameters whose are the dependencies of this expression.
        """
        return []

    @property
    @abstractmethod
    def complex(self) -> bool:
        """
        :returns: True if the expression is a complex one, else False.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def expr_raw(self):
        """
        :returns: the raw version of the expression.
        """
        raise NotImplementedError()

    @abstractmethod
    def evaluate(
        self, dependencies_values: Dict[str, Union[float, int, str]]
    ) -> Union[float, int, str]:
        """
        Evaluate this expression and return the evaluated value.

        :param dependencies_values: the values of the dependencies of this expression.
        """
        raise NotImplementedError()


class ImpactModelFloatConst(ImpactModelExpr):
    """
    Represent a float type constant.
    """

    value: float

    @property
    def complex(self) -> bool:
        return False

    @property
    def expr_raw(self):
        return self.value

    def evaluate(
        self, dependencies_values: Dict[str, Union[float, int, str]]
    ) -> Union[float, int, str]:
        return self.value


class ImpactModelEnumConst(ImpactModelExpr):
    """
    Represents an constant enum type.
    """

    value: str

    @property
    def complex(self) -> bool:
        return False

    @property
    def expr_raw(self):
        return self.value

    def evaluate(
        self, dependencies_values: Dict[str, Union[float, int, str]]
    ) -> Union[float, int, str]:
        return self.value


class ImpactModelFloatExpr(ImpactModelExpr):
    """
    Represents a float type expression.
    """

    expr: str

    @classmethod
    def parse(
        cls,
        raw_expr: Union[float, int, str, dict],
        param: str,
        params_infos: Dict[str, dict],
    ) -> ImpactModelExpr:
        if not validate_expr(raw_expr):
            raise InvalidExpr("float_expr", raw_expr)
        expr = ImpactModelFloatExpr(**{"expr": raw_expr})
        deps = set(expr.dependencies)
        # Check all the dependencies are parameters of the impact model
        invalid_deps = sorted(deps - params_infos.keys())
        if invalid_deps:
            raise InvalidExpr(
                "no_such_param",
                raw_expr,
                {"invalid_parameters": tuple(invalid_deps)},
            )
        # Check all the dependencies are float type parameters
        non_float_deps = sorted(
            [dep for dep in deps if dep not in params_infos[dep]["type"] != "float"]
        )
        if non_float_deps:
            raise InvalidExpr(
                "dependencies_type",
                raw_expr,
                {
                    "invalid_parameters": tuple(non_float_deps),
                    "required_type": "float",
                },
            )
        return expr

    @property
    def dependencies(self) -> List[str]:
        return re.findall(r"[a-zA-Z_]+\b(?!\()", self.expr)

    @property
    def complex(self) -> bool:
        return True

    @property
    def expr_raw(self):
        return self.expr

    def evaluate(
        self, dependencies_values: Dict[str, Union[float, int, str]]
    ) -> Union[float, int, str]:
        return sympify(self.expr).evalf(subs=dependencies_values)


class ImpactModelEnumExpr(ImpactModelExpr):
    """
    Represents an enum type expression.
    """

    param: str
    options: Dict[str, ImpactModelExpr]

    @classmethod
    def parse(
        cls,
        raw_expr: Union[float, int, str, dict],
        param: str,
        params_infos: Dict[str, dict],
    ) -> ImpactModelExpr:
        # Check only one parameter is used
        deps = list(raw_expr.keys())
        if len(deps) != 1:
            raise InvalidExpr(
                "too_much_dependencies", raw_expr, {"required": 1, "value": len(deps)}
            )
        dep = deps[0]
        # Check the parameter is a parameter of the impact model
        if dep not in params_infos.keys():
            raise InvalidExpr("no_such_param", raw_expr, {"invalid_parameters": (dep,)})
        # Check the parameter is an enum type
        if params_infos[dep]["type"] != "enum":
            raise InvalidExpr(
                "dependencies_type",
                raw_expr,
                {"invalid_parameters": (dep,), "required_type": "enum"},
            )
        dep_options = set(params_infos[dep]["options"])
        options = raw_expr[dep]
        # Check for none options
        none_options = sorted(
            [option for option, sub_expr in options.items() if sub_expr is None]
        )
        if none_options:
            raise InvalidExpr(
                "enum_expr_empty_options",
                raw_expr,
                {"invalid_options": tuple(none_options)},
            )
        # Parse options
        options = {
            option: ImpactModelExpr.parse(sub_expr, param, params_infos)
            for option, sub_expr in options.items()
        }
        # Check for missing options
        missing_options = sorted(dep_options - options.keys())
        if missing_options:
            raise InvalidExpr(
                "enum_expr_options",
                raw_expr,
                {
                    "missing_options": tuple(missing_options),
                    "extra_options": (),
                },
            )
        # Check there is no extra options
        extra_options = sorted(options.keys() - dep_options)
        if extra_options:
            raise InvalidExpr(
                "enum_expr_options",
                raw_expr,
                {
                    "missing_options": (),
                    "extra_options": tuple(extra_options),
                },
            )
        return ImpactModelEnumExpr(**{"param": dep, "options": options})

    @property
    def dependencies(self) -> List[str]:
        deps = {self.param}
        for sub_expr in self.options.values():
            deps = deps | set(sub_expr.dependencies)
        return deps

    @property
    def complex(self) -> bool:
        return True

    @property
    def expr_raw(self):
        return {
            self.param: {
                option: sub_expr.expr_raw for option, sub_expr in self.options.items()
            }
        }

    def evaluate(
        self, dependencies_values: Dict[str, Union[float, int, str]]
    ) -> Union[float, int, str]:
        return self.options[dependencies_values[self.param]].evaluate(
            dependencies_values
        )
