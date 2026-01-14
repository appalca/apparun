from __future__ import annotations

from typing import Dict, List, Optional, Set, Union

import pandas as pd
from pydantic import BaseModel

from apparun.exceptions import InvalidFileError
from apparun.impact_methods import MethodUniqueScore
from apparun.logger import logger


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

    def to_normalisation(
        self,
        method: Optional[MethodUniqueScore] = MethodUniqueScore.EF30,
        filenorm: Optional[str] = None,
    ) -> LCIAScores:
        """
        Computes normalisation of LCIAScores using .csv file with impact categories and normalisation factors.
        :param: method -> allows to use default MethodUniqueScore.EF30 or EF31 normalisation factors.
        :param: filenorm -> allows to give a personal .csv file with normalisation factors.
        """
        if filenorm is None:
            filenorm = method.path_to_norm()
            logger.warning(f"No given normalisation file, using default {filenorm}")
        score = LCIAScores(scores=self.scores.copy())
        normalisation_factor = pd.read_csv(filenorm).sort_values(by=["method"])
        normalisation_factor = normalisation_factor[
            normalisation_factor["method"].isin(score.scores.keys())
        ].set_index("method", drop=True)
        if len(normalisation_factor) != len(score.scores.keys()):
            raise InvalidFileError(filenorm)
        for method_name in score.scores.keys():
            for i in range(0, len(score.scores[method_name])):
                score.scores[method_name][i] = (
                    score.scores[method_name][i]
                    / normalisation_factor.at[method_name, "score"]
                )

        return LCIAScores(scores=score.scores)

    def to_weighting(
        self,
        method: Optional[MethodUniqueScore] = MethodUniqueScore.EF30,
        fileweight: Optional[str] = None,
    ) -> LCIAScores:
        """
        Computes normalisation of LCIAScores using .csv file with impact categories and normalisation factors.
        :param: method -> allows to use default MethodUniqueScore.EF30 or EF31 weighting factors.
        :param: fileweight -> allows to give a personal .csv file with weighting factors.
        """
        if fileweight is None:
            fileweight = method.path_to_weight()
            logger.warning(f"No given weighting file, using default {fileweight}")
        score = LCIAScores(scores=self.scores.copy())
        weighting_factor = pd.read_csv(fileweight).sort_values(by=["method"])
        weighting_factor = weighting_factor[
            weighting_factor["method"].isin(score.scores.keys())
        ].set_index("method", drop=True)
        if len(weighting_factor) != len(score.scores.keys()):
            raise InvalidFileError(fileweight)

        for method_name in score.scores.keys():
            for i in range(0, len(score.scores[method_name])):
                score.scores[method_name][i] = (
                    score.scores[method_name][i]
                    * weighting_factor.at[method_name, "score"]
                )

        return LCIAScores(scores=score.scores)

    def to_unique_score(
        self,
        isNorm: Optional[bool] = False,
        isWeight: Optional[bool] = False,
        method: Optional[MethodUniqueScore] = MethodUniqueScore.EF30,
        filenorm: Optional[str] = None,
        fileweight: Optional[str] = None,
    ) -> LCIAScores:
        """
        Computes sum of LCIAScores impact category scores into unique score. Possible to apply normalisation
        and/or weighting before aggregating scores.
        :param: isNorm = True -> apply normalisation before sum into unique score.
        :param: isWeight = True -> apply weighting (after normalisation) before sum into unique score.
        :param: method -> allows to use default MethodUniqueScore.EF30 or EF31 normalisation and weighting factors.
        :param: filenorm -> allows to give a personal .csv file with normalisation factors.
        :param: fileweight -> allows to give a personal .csv file with weighting factors.
        """
        score = LCIAScores(scores=self.scores.copy())
        if isNorm is not False:
            score = score.to_normalisation(method=method, filenorm=filenorm)
        if isWeight is not False:
            score = score.to_weighting(method=method, fileweight=fileweight)

        sum_score = [sum(x) for x in zip(*score.scores.values())]
        unique_score = {"UNIQUE_SCORE": sum_score}
        return LCIAScores(scores=unique_score)

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
