from __future__ import annotations

from typing import Callable, Dict, List, Optional, Union

import numpy as np
import yaml
from pydantic import BaseModel
from SALib.analyze import sobol

from apparun.impact_tree import ImpactTreeNode
from apparun.parameters import ImpactModelParams
from apparun.score import LCIAScores
from apparun.tree_node import NodeScores


class LcaPractitioner(BaseModel):
    """
    Information about a LCA practitioner.
    """

    name: Optional[str] = None
    organization: Optional[str] = None
    mail: Optional[str] = None


class LcaStudy(BaseModel):
    """
    Information about LCA study, in order to understand its scope and for
    reproducibility.
    """

    link: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None
    version: Optional[str] = None
    license: Optional[str] = None
    appabuild_version: Optional[str] = None


class ModelMetadata(BaseModel):
    """
    Contain information various information about the context of production of the
    impact model.
    """

    author: Optional[LcaPractitioner] = None
    reviewer: Optional[LcaPractitioner] = None
    report: Optional[LcaStudy] = None

    def to_dict(self):
        """
        Convert self to dict.
        :return: self as a dict
        """
        return self.model_dump()

    @staticmethod
    def from_dict(model_metadata: dict) -> ModelMetadata:
        """
        Convert dict to ModelMetadata object.
        :param model_metadata: dict containing construction parameters of the model
        metadata.
        :return: constructed model metadata.
        """
        return ModelMetadata(
            author=LcaPractitioner(**model_metadata["author"]),
            reviewer=LcaPractitioner(**model_metadata["reviewer"]),
            report=LcaStudy(**model_metadata["report"]),
        )


class ImpactModel(BaseModel):
    """
    Impact model contains all the information required to compute the impact of an
    LCA built with Appa Build.
    """

    metadata: Optional[ModelMetadata] = None
    parameters: Optional[ImpactModelParams] = None
    tree: Optional[ImpactTreeNode] = None

    @property
    def name(self):
        return self.tree.name

    @property
    def transformation_table(
        self,
    ) -> Dict[str, Callable[[Union[str, float]], Dict[str, float]]]:
        """
        Map each parameter to its transform method.
        :return: a dict mapping impact model's parameters' name with their transform
        method.
        """
        return {parameter.name: parameter.transform for parameter in self.parameters}

    def transform_parameters(
        self, parameters: Dict[str, Union[List[Union[str, float]], Union[str, float]]]
    ) -> Dict[str, Union[List[Union[str, float]], Union[str, float]]]:
        """
        Transform all the parameters' values, so it can be fed into a node's compute
        method. See ImpactModelParam's transform methods for more information.
        :param parameters: a dict mapping parameters' name and parameters' value, or
        list of values.
        :return: a dict mapping parameters' name and parameters' transformed value, or
        list of transformed values.
        """
        list_parameters = {
            name: parameter
            for name, parameter in parameters.items()
            if isinstance(parameter, list)
        }
        single_parameters = {
            name: parameter
            for name, parameter in parameters.items()
            if not isinstance(parameter, list)
        }
        if len(list_parameters) == 0:
            return {
                name: value
                for table in [
                    self.transformation_table[parameter_name](parameter_value)
                    for parameter_name, parameter_value in parameters.items()
                ]
                for name, value in table.items()
            }
        assert min(
            len(list_parameter) for list_parameter in list_parameters.values()
        ) == max(len(list_parameter) for list_parameter in list_parameters.values())
        full_list_parameters = {
            **{
                parameter_name: [parameter_value]
                * len(list(list_parameters.values())[0])
                for parameter_name, parameter_value in single_parameters.items()
            },
            **list_parameters,
        }
        return {
            name: value
            for table in [
                self.transformation_table[parameter_name](parameter_value)
                for parameter_name, parameter_value in full_list_parameters.items()
            ]
            for name, value in table.items()
        }

    def to_dict(self):
        """
        Convert self to dict.
        :return: self as a dict
        """
        return {
            "metadata": self.metadata.to_dict(),
            "parameters": self.parameters.to_list(sorted_by_name=True),
            "tree": self.tree.to_dict(),
        }

    def to_yaml(self, filepath: str, compile_models: bool = True):
        """
        Convert self to yaml file.
        :param filepath: filepath of the yaml file to create.
        :param compile_models: if True, all models in tree nodes will be compiled.
        ImpactModel will be bigger, but its execution will be faster at first use.
        """
        if compile_models:
            self.tree.compile_models()
        with open(filepath, "w") as stream:
            yaml.dump(self.to_dict(), stream, sort_keys=False)

    @staticmethod
    def from_dict(impact_model: dict) -> ImpactModel:
        """
        Convert dict to ImpactModel object.
        :param impact_model: dict containing construction parameters of the impact
        model.
        :return: constructed impact model.
        """
        return ImpactModel(
            metadata=ModelMetadata.from_dict(impact_model["metadata"]),
            parameters=ImpactModelParams.from_list(impact_model["parameters"]),
            tree=ImpactTreeNode.from_dict(impact_model["tree"]),
        )

    def from_tree_children(self) -> List[ImpactModel]:
        """
        Create a new impact model for each of Impact Model tree root node's children.
        Parameters of the impact model are copied, so unused parameters can remain in
        newly created impact models.
        :return: a list of newly created impact models.
        """
        return [
            ImpactModel(parameters=self.parameters, tree=child)
            for child in self.tree.children
        ]

    @staticmethod
    def from_yaml(filepath: str) -> ImpactModel:
        """
        Convert a yaml file to an ImpactModel object.
        :param filepath: yaml file containing construction parameters of the impact
        model.
        :return: constructed impact model.
        """
        with open(filepath, "r") as stream:
            impact_model = yaml.safe_load(stream)
            return ImpactModel.from_dict(impact_model)

    def get_scores(self, **params) -> LCIAScores:
        """
        Get impact scores of the root node for each impact method, according to the
        parameters.
        :param params: value, or list of values of the impact model's parameters.
        List of values must have the same length. If single values are provided
        alongside a list of values, it will be duplicated to the appropriate length.
        :return: a dict mapping impact names and corresponding score, or list of scores.
        """
        missing_params = self.parameters.get_missing_parameter_names(params)
        default_params = self.parameters.get_default_values(missing_params)
        transformed_params = self.transform_parameters({**params, **default_params})
        scores = self.tree.compute(transformed_params)
        return scores

    def get_nodes_scores(
        self, by_property: Optional[str] = None, **params
    ) -> List[NodeScores]:
        """
        Get impact scores of the each node for each impact method, according to the
        parameters.
        :param by_property: if different than None, results will be pooled by nodes
        sharing the same property value. Property name is the value of by_property.
        :param params: value, or list of values of the impact model's parameters.
        List of values must have the same length. If single values are provided
        alongside a list of values, it will be duplicated to the appropriate length.
        :return: a list of dict mapping impact names and corresponding score, or list
        of scores, for each node/property value.
        """
        missing_params = self.parameters.get_missing_parameter_names(params)
        default_params = self.parameters.get_default_values(missing_params)
        transformed_params = self.transform_parameters({**params, **default_params})
        scores = [
            NodeScores(
                name=node.name,
                properties=node.properties,
                parent=node.parent.name if node.parent is not None else "",
                lcia_scores=node.compute(
                    transformed_params, direct_impacts=by_property is not None
                ),
            )
            for node in self.tree.unnested_descendants
        ]
        if by_property is not None:
            scores = NodeScores.combine_by_property(scores, by_property)
        return scores

    def get_uncertainty_nodes_scores(self, n) -> List[NodeScores]:
        """ """
        samples = self.parameters.uniform_draw(n)
        samples = self.parameters.draw_to_distrib(samples)
        nodes_scores = self.get_nodes_scores(**samples)
        return nodes_scores

    def get_uncertainty_scores(self, n) -> LCIAScores:
        """ """
        samples = self.parameters.uniform_draw(n)
        samples = self.parameters.draw_to_distrib(samples)
        lcia_scores = self.get_scores(**samples)
        return lcia_scores

    def get_sobol_s1_indices(
        self, n, all_nodes: bool = False
    ) -> List[Dict[str, Union[str, np.ndarray]]]:
        """
        Get sobol first indices, which corresponds to the contribution of each
        parameter to total result variance.
        :param n: number of samples to draw with monte carlo.
        :param all_nodes: if True, sobol s1 indices will be computed for each node. Else,
        only for root node (FU).
        :return: unpivoted dataframe containing sobol first indices for each parameter,
        impact method, and node name if all_nodes is True.
        """
        samples = self.parameters.sobol_draw(n)
        samples = self.parameters.draw_to_distrib(samples)
        if all_nodes:
            lcia_scores = self.get_nodes_scores(**samples)
            sobol_s1_indices = []
            for node_scores in lcia_scores:
                for method, scores in node_scores.lcia_scores.scores.items():
                    s1 = sobol.analyze(
                        self.parameters.sobol_problem,
                        np.array(scores),
                        calc_second_order=True,
                    )["S1"]
                    sobol_s1_indices += [
                        {
                            "node": node_scores.name,
                            "method": method,
                            "parameter": self.parameters.sobol_problem["names"][i],
                            "sobol_s1": s1[i],
                        }
                        for i in range(len(s1))
                    ]
            return sobol_s1_indices
        lcia_scores = self.get_scores(**samples)
        sobol_s1_indices = []
        for method, scores in lcia_scores.scores.items():
            s1 = sobol.analyze(
                self.parameters.sobol_problem, np.array(scores), calc_second_order=True
            )["S1"]
            sobol_s1_indices += [
                {
                    "node": self.tree.name,
                    "method": method,
                    "parameter": self.parameters.sobol_problem["names"][i],
                    "sobol_s1": s1[i],
                }
                for i in range(len(s1))
            ]
        return sobol_s1_indices
