from __future__ import annotations

import itertools
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Union

import numpy as np
from pydantic import BaseModel
from sympy import Expr, lambdify, parse_expr

from apparun.score import LCIAScores
from apparun.tree_node import NodeProperties


class ImpactTreeNode(BaseModel):
    """
    Impact Model tree node representing the impacts of an activity as well as its
    children.
    """

    name: str
    amount: Optional[Union[Expr, float]] = None
    direct_impacts: Optional[Dict[str, Expr]] = {}
    scaled_direct_impacts: Optional[Dict[str, Expr]] = {}
    models: Optional[Dict[str, Expr]] = {}
    parent: Optional[ImpactTreeNode] = None
    children: Optional[List[ImpactTreeNode]] = []
    properties: NodeProperties = NodeProperties(properties={})
    _raw_direct_impact: Optional[Expr] = None
    _combined_amount: Optional[Union[Expr, float]] = None

    class Config:
        arbitrary_types_allowed = True

    @property
    def models_compiled(self):
        return len(self.models) > 0 and len(self.scaled_direct_impacts) > 0

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

    def compile_models(self):
        """
        Replace descendants symbols in node's model by their corresponding model.
        Result is stored in "compiled_model" node's attribute.
        """
        self.scaled_direct_impacts = {
            method: self.combined_amount * direct_impact
            for method, direct_impact in self.direct_impacts.items()
        }
        self.models = self.scaled_direct_impacts
        for child in self.children:
            child.compile_models()
            self.models = {
                method: model + child.models[method]
                for method, model in self.models.items()
            }

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
        :param compile: if True, all models in tree nodes will be compiled. ImpactModel
        will be bigger, but its execution will be faster at first use.
        :return: self as a dict
        """
        return {
            "name": self.name,
            "models": {
                str(method): str(model) for method, model in self.models.items()
            },
            "direct_impacts": {
                str(method): str(model) for method, model in self.direct_impacts.items()
            },
            "scaled_direct_impacts": {
                str(method): str(model)
                for method, model in self.scaled_direct_impacts.items()
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
        node = ImpactTreeNode(
            name=impact_model_tree_node["name"],
            models={
                method: parse_expr(expr)
                for method, expr in impact_model_tree_node["models"].items()
            },
            direct_impacts={
                method: parse_expr(expr)
                for method, expr in impact_model_tree_node["direct_impacts"].items()
            },
            scaled_direct_impacts={
                method: parse_expr(expr)
                for method, expr in impact_model_tree_node[
                    "scaled_direct_impacts"
                ].items()
            },
            properties=NodeProperties.from_dict(impact_model_tree_node["properties"]),
            amount=parse_expr(impact_model_tree_node["amount"]),
        )
        for child in impact_model_tree_node["children"]:
            node.new_child_from_dict(child)
        return node

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
        ],
        direct_impacts: bool = False,
    ) -> LCIAScores:
        """
        Compute node's impacts with given parameters values.
        Multithreading is used to compute different impact methods in parallel.
        :param transformed_params: parameters, transformed by ImpactModelParam's
        transform method.
        :param direct_impacts: if True, direct_impacts will be computed instead of
        full impacts (i.e. sum of direct impacts and children direct impacts)
        :return: a dict mapping impact's name with corresponding score, or list of
        scores.
        """
        if not self.models_compiled:
            self.compile_models()
        if direct_impacts:
            lambda_models = {
                method: lambdify(
                    [param for param in transformed_params], model, modules=["numpy"]
                )
                for method, model in self.scaled_direct_impacts.items()
            }
        else:
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

        if len(params)==0:
            return {method_name: result}

        if isinstance(list(params.values())[0], np.ndarray) and not isinstance(
            result, np.ndarray
        ):
            result = np.repeat(result, len(list(params.values())[0]))
        return {method_name: result}
