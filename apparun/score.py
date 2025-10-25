from __future__ import annotations

from typing import Dict, List, Optional, Set, Union

import pandas as pd
from pydantic import BaseModel


class LCIAScores(BaseModel):
    """
    Scores for each impact method.
    """

    scores: Optional[Dict[str, Union[float, List[float]]]] = {}

    @property
    def method_names(self) -> Set[str]:
        """
        Get all LCIA methods assessed.
        :return: LCIA methods assessed
        """
        return set(self.scores.keys())

    def to_unpivoted_df(self) -> pd.DataFrame:
        if isinstance(list(self.scores.values())[0], float) or isinstance(
            list(self.scores.values())[0], float
        ):
            df = pd.DataFrame(self.scores, index=[0])
        else:
            df = pd.DataFrame(self.scores)
        df = pd.melt(df, var_name="method", value_name="score")
        return df

    def __add__(self, other) -> LCIAScores:
        scores = {
            method_name: self.scores[method_name] + other.scores[method_name]
            if isinstance(self.scores[method_name], float)
            else [
                self.scores[method_name][i] + other.scores[method_name][i]
                if method_name in other.scores
                else self.scores[method_name][i]
                for i in range(len(self.scores[method_name]))
            ]
            for method_name in self.scores.keys()
        }
        return LCIAScores(scores=scores)

    def __sub__(self, other) -> LCIAScores:
        scores = {
            method_name: self.scores[method_name] - other.scores[method_name]
            if isinstance(self.scores[method_name], float)
            else [
                self.scores[method_name][i] - other.scores[method_name][i]
                if method_name in other.scores
                else self.scores[method_name][i]
                for i in range(len(self.scores[method_name]))
            ]
            for method_name in self.scores.keys()
        }
        return LCIAScores(scores=scores)

    @staticmethod
    def sum(lcia_scores: List[LCIAScores]) -> LCIAScores:
        """
        Sum element-wise all scores for each method.
        :param lcia_scores: LCIA scores to sum up.
        :return: summed LCIA scores
        """
        if len(lcia_scores) == 0:
            return LCIAScores()
        scores = {
            method_name: [lcia_score.scores[method_name] for lcia_score in lcia_scores]
            for method_name in lcia_scores[0].method_names
        }
        scores = {
            method_name: sum(score)
            if isinstance(score[0], float)
            else [sum(x) for x in zip(*score)]
            for method_name, score in scores.items()
        }
        return LCIAScores(scores=scores)
