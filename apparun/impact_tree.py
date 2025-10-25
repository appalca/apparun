from __future__ import annotations

import itertools
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional, Self, Union

import numpy as np
from pydantic import BaseModel, ValidationError, field_validator
from pydantic_core import PydanticCustomError
from sympy import Expr, lambdify

from apparun.exceptions import InvalidExpr
from apparun.expressions import parse_expr
from apparun.logger import logger
from apparun.score import LCIAScores
from apparun.tree_node import NodeProperties


class ImpactTreeNode(BaseModel):
    """
    Impact Model tree node representing the impacts of an activity as well as its
    children.
    """

    name: str
    amount: Optional[Union[Expr, float]] = None
    models: Optional[Dict[str, Expr]] = {}
    parent: Optional[ImpactTreeNode] = None
    children: Optional[List[ImpactTreeNode]] = []
    properties: NodeProperties = NodeProperties(properties={})
    _raw_direct_impact: Optional[Expr] = None
    _combined_amount: Optional[Union[Expr, float]] = None

    class Config:
        arbitrary_types_allowed = True

    @field_validator("amount", mode="before")
    @classmethod
    def validate_amount(
        cls, amount: Union[float, int, str, Expr]
    ) -> Union[Expr, float]:
        try:
            if isinstance(amount, (float, int, Expr)):
                return amount
            return parse_expr(amount)
        except InvalidExpr:
            raise PydanticCustomError("float_expr", "Invalid float expression")

    @field_validator("models", mode="before")
    @classmethod
    def validate_exprs(cls, exprs: Dict[str, str]) -> Dict[str, Expr]:
        try:
            for key, expr in exprs.items():
                exprs[key] = parse_expr(expr)
        except InvalidExpr as e:
            raise PydanticCustomError("invalid_expr", "", {"expr": e.expr})
        return exprs

    @property
    def unnested_descendants(self) -> List[ImpactTreeNode]:
        """
        Walk recursively through node's children to return a list of all its
        descendants.
        :return: a list containing current node and all its descendants.
        """
        return list(
            itertools.chain.from_iterable(
                [child.unnested_descendants for child in self.children]
            )
        ) + [self]

    @property
    def combined_amount(self) -> Union[float, Expr]:
        if self.parent is None:
            return self.amount
        if self._combined_amount is None:
            self._combined_amount = self.amount * self.parent.combined_amount
        return self._combined_amount

    def new_child(self, **args) -> ImpactTreeNode:
        """
        Build a new node as a child.
        :param args: construction parameters of new node.
        :return: constructed node
        """
        child = ImpactTreeNode(**args, parent=self)
        self.children.append(child)
        return child

    def new_child_from_dict(self, child: dict) -> ImpactTreeNode:
        """
        Build a new node as a child.
        :param child: dict containing construction parameters of new node.
        :return: constructed node
        """
        child = ImpactTreeNode.from_dict(child)
        child.parent = self
        self.children.append(child)
        return child

    def name_already_in_tree(self, name: str) -> bool:
        """
        Check if a node exists in descendants by comparing names.
        :param name: name to check presence in descendants
        :return: a boolean indicating if a descendant already has requested name.
        """
        return (
            False
            if self.parent is None and self.name != name
            else self.parent.name_already_in_tree(name)
        )

    def to_dict(self) -> dict:
        """
        Convert self to dict.
        :return: self as a dict
        """
        return {
            "name": self.name,
            "models": {
                str(method): str(model) for method, model in self.models.items()
            },
            "children": [child.to_dict() for child in self.children],
            "properties": self.properties.properties,
            "amount": str(self.amount),
        }

    @staticmethod
    def from_dict(impact_model_tree_node: dict) -> ImpactTreeNode:
        """
        Convert dict to ImpactTreeNode object.
        :param impact_model_tree_node: dict containing construction parameters of the
        node.
        :return: constructed node
        """
        try:
            node = ImpactTreeNode(
                name=impact_model_tree_node["name"],
                models=impact_model_tree_node["models"],
                properties=NodeProperties.from_dict(
                    impact_model_tree_node["properties"]
                ),
                amount=impact_model_tree_node["amount"],
            )
            for child in impact_model_tree_node["children"]:
                node.new_child_from_dict(child)
            return node
        except ValidationError as e:
            for err in e.errors():
                if err["type"] == "float_expr":
                    logger.error(
                        "Invalid expression in the tree node %s: %s",
                        err["loc"][0],
                        err["input"],
                    )
            raise

    @staticmethod
    def node_name_to_symbol_name(node_name: str) -> str:
        """
        Convert node name to symbol name by replacing everything which is not an
        alphanumerical character by an underscore.
        :param node_name: node's name
        :return: symbol's name
        """
        return re.sub("[^0-9a-zA-Z]+", "_", node_name)

    def compute(
        self,
        transformed_params: Dict[
            str, Union[List[Union[str, float]], Union[str, float]]
        ]
    ) -> LCIAScores:
        """
        Compute node's impacts with given parameters values.
        Multithreading is used to compute different impact methods in parallel.
        :param transformed_params: parameters, transformed by ImpactModelParam's
        transform method.
        :return: a dict mapping impact's name with corresponding score, or list of
        scores.
        """
        lambda_models = {
            method: lambdify(
                [param for param in transformed_params], model, modules=["numpy"]
            )
            for method, model in self.models.items()
        }
        results = {}
        with ThreadPoolExecutor() as executor:
            futures = []
            for method_name, lambda_model in lambda_models.items():
                futures.append(
                    executor.submit(
                        self._multithread_compute_process,
                        method_name=method_name,
                        lambda_model=lambda_model,
                        **transformed_params,
                    )
                )
            for future in as_completed(futures):
                results.update(future.result())

        if isinstance(list(results.values())[0], np.ndarray):
            results_ = results.copy()
            results.update({key: value.tolist() for key, value in results_.items()})
        return LCIAScores(scores=results)

    @staticmethod
    def _multithread_compute_process(method_name, lambda_model, **params):
        """
        Execute a lambda model with given params.
        :param method_name: impact method's name.
        :param lambda_model: model to execute.
        :param params: parameters of the lambda model.
        :return: a dict mapping results with method's name.
        """
        result = lambda_model(**params)
        # Lambdified model returns a constant if model is a constant itself.
        # Need to convert it to ndarray.

        if len(params) == 0:
            return {method_name: result}

        if isinstance(list(params.values())[0], np.ndarray) and not isinstance(
            result, np.ndarray
        ):
            result = np.repeat(result, len(list(params.values())[0]))
        return {method_name: result}
