from __future__ import annotations

from typing import Dict, List, Optional, Set, Union

import pandas as pd
from pydantic import BaseModel

from apparun.score import LCIAScores


class NodeProperties(BaseModel):
    """
    Properties of an impact model node. Can be used by to break the results down
    according to life cycle phase, for exemple. Properties can be key/value
    (ex: {"phase": "production"} or flags (ex: {production_phase: True}).
    """

    properties: Dict[str, Union[str, float, bool]] = {}

    @classmethod
    def from_dict(
        cls, properties: Dict[str, Union[str, float, bool]]
    ) -> NodeProperties:
        """
        Construct using dict.
        :param properties: properties of the node.
        :return: constructed NodeProperties
        """
        return NodeProperties(properties=properties)

    def get_property_value(self, property_name: str) -> Optional[Union[str, bool]]:
        """
        Gives the value of a property by name, returns None if property doesn't exist.
        :param property_name: name of the property to get value
        :return: value of the property, None if doesn't exist
        """
        return (
            self.properties[property_name] if property_name in self.properties else None
        )


class NodeScores(BaseModel):
    """
    Gathers all useful information to exploit computed node wise LCIA results.
    """

    name: str
    "Node name/property value, if results have been combined by property value."
    parent: str
    "Name of parent node."
    properties: NodeProperties
    "Properties of the node."
    lcia_scores: LCIAScores
    "Computed LCIA scores, for each method."

    @staticmethod
    def combine_by_property(
        nodes_scores: List[NodeScores], property_name: str
    ) -> List[NodeScores]:
        """
        Sum up (element wise) the scores of each node sharing the same property value,
        for each method.
        :param nodes_scores: node scores to combine according to property value.
        :param property_name: name of the property under consideration
        :return: list of newly created nodes. Name of the node will be the property
        value.
        """
        all_values = set(
            [
                node.properties.get_property_value(property_name)
                for node in nodes_scores
                if len(node.properties.properties) > 0
            ]
        )
        nodes_by_value = {
            value: [
                node
                for node in nodes_scores
                if node.properties.get_property_value(property_name) == value
            ]
            for value in all_values
        }
        scores_by_values = {
            value: LCIAScores.sum([node.lcia_scores for node in nodes])
            for value, nodes in nodes_by_value.items()
        }
        return [
            NodeScores(
                name=str(value),
                parent="",
                properties=NodeProperties(),
                lcia_scores=scores_by_values[value],
            )
            for value in all_values
        ]

    def to_unpivoted_df(self) -> pd.DataFrame:
        df = self.lcia_scores.to_unpivoted_df()
        df["name"] = self.name
        df["parent"] = self.parent
        return df
