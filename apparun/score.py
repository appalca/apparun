from __future__ import annotations

from typing import Dict, List, Optional, Set, Union

import pandas as pd
from pydantic import BaseModel
from apparun.logger import logger
from apparun.exceptions import InvalidNormFileError

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
    
    def to_unique_score_df(
            self, 
            filenorm: str, 
            fileweight: Optional[str] = None, 
            u_sum: Optional[bool] = False
            ) -> pd.DataFrame:
        """ 
        Computes normalisation, weighting and sum of each impact category 
        to obtain unique score. 
        :param filenorm: file path to .csv containing normalisation factors. 
        :param fileweight: file path to .csv containing weighting factors.
        :u_sum: if True, function returns unique score after sum. Otherwise, 
        returns normalised and weighting results for each impact category.
        """
        scores = self.to_unpivoted_df()

        # Verify data from normalisation and weighting files
        normalisation_factor = pd.read_csv(filenorm).sort_values(by=['method'], ignore_index=True)
        if scores['method'].nunique() != normalisation_factor['method'].nunique():
            raise InvalidNormFileError (filenorm, normalisation_factor['method'].nunique(), scores['method'].nunique())
        if (scores['method'].sort_values(ignore_index=True).unique()==normalisation_factor['method'].to_numpy()).all()==False:
            logger.warning(f'Warning: Impact category names from {filenorm} different from model. Check correspondances.') 

        if fileweight is not None :
            weighting_factor = pd.read_csv(fileweight).sort_values(by=['method'], ignore_index=True)
            if scores['method'].nunique() == weighting_factor['method'].nunique():
                if (scores['method'].sort_values(ignore_index=True).unique()==weighting_factor['method'].to_numpy()).all()==False:
                    logger.warning(f'Warning: Impact category names from {fileweight} different from model. Check correspondance.')
            else:
                weighting_factor = normalisation_factor.copy()
                weighting_factor['score'] = 1
                logger.warning(f'Number of impact categories from {fileweight} != model. Weighting not applied')
        else :
            weighting_factor = normalisation_factor.copy()
            weighting_factor['score'] = 1
            logger.warning("Warning: no file for weights. Weighting not applied.")

        # Compute normalisation, weighting and sum depending on parameters
        nb_par_scores = (scores['method']==scores['method'].iloc[0]).sum() 
        score = scores.iloc[lambda x: x.index % nb_par_scores == 0].get(["method"]).sort_values(by=['method'], ignore_index=True) # initialise df w/ columns 
        if u_sum is True:
            unique_score = pd.DataFrame(data={'method':['EFV3_UNIQUE_SCORE']})
        for i in range (0, nb_par_scores) :
            tmp = scores.iloc[lambda x: x.index % nb_par_scores == i].sort_values(by=['method'], ignore_index=True) 
            tmp['score'] =  tmp['score'] / normalisation_factor['score'] * weighting_factor['score']
            score.insert(i+1, "score", tmp.get("score"), allow_duplicates=True)
            if u_sum is True:
                unique_score.insert(i+1, "score", sum(tmp['score']), allow_duplicates=True)
        if u_sum is True:
            return unique_score
        else :
            return score

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
