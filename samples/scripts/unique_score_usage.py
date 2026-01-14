import os

import pandas as pd

from apparun.impact_methods import MethodUniqueScore
from apparun.impact_model import ImpactModel
from apparun.results import (
    ImpactModelResult,
    NodesUncertaintyResult,
    get_result,
    register_result,
)
from apparun.score import LCIAScores
from apparun.tree_node import NodeProperties, NodeScores

"""
Python script to demonstrate the use of to_normalisation(), to_weighting(), and
to_unique_score() functions.
Demonstration on hardcoded LCIAScores impact values, but all functions can be
applied to ImpactModel.get_scores() or ImpactModel.get_nodes_scores() LCIAScores
outputs.
"""
# Equivalent to impact_model.get_scores() outputs with 16 PEF impact categories
score_init = LCIAScores()
score_init.scores = {
    "EFV3_IONISING_RADIATION": [0.6068699279546468],
    "EFV3_CLIMATE_CHANGE": [0.48099441376098245],
    "EFV3_ECOTOXICITY_FRESHWATER": [25.623842167732157],
    "EFV3_ACIDIFICATION": [0.003207360438923497],
    "EFV3_PARTICULATE_MATTER_FORMATION": [1.93010983477257e-08],
    "EFV3_EUTROPHICATION_FRESHWATER": [0.0002181131078252415],
    "EFV3_EUTROPHICATION_MARINE": [0.0004682480530574293],
    "EFV3_HUMAN_TOXICITY_CARCINOGENIC": [1.5157566744991439e-10],
    "EFV3_PHOTOCHEMICAL_OZONE_FORMATION": [0.0014206161263303997],
    "EFV3_OZONE_DEPLETION": [1.343167709082962e-07],
    "EFV3_EUTROPHICATION_TERRESTRIAL": [0.004685951302088373],
    "EFV3_MATERIAL_RESOURCES": [5.455787785777846e-05],
    "EFV3_HUMAN_TOXICITY_NON_CARCINOGENIC": [9.61544194332376e-09],
    "EFV3_LAND_USE": [1.1607977689437137],
    "EFV3_WATER_USE": [0.33907075531438513],
    "EFV3_ENERGY_RESOURCES": [18.16667409731127],
}

# print LCIAScores with DataFrame format for better visualisation
print(score_init.to_unpivoted_df())

# Apply normalisation with default normalisation factor method -> using PEF3.0 available normalisation factors
score = score_init.to_normalisation()
# Apply weighting with weighting factors from file 'apparun/resources/pef30/weighting_factor.csv'
score = score.to_weighting(fileweight="apparun/resources/pef30/weighting_factor.csv")
# Sup all impact category scores
score = score.to_unique_score()
print(score.to_unpivoted_df())

# 3 previous functions can be called with only to_unique_score() specifying isNorm and isWeight to True
# Apply normalisation with normalisation EF30 factor method (EF31 also available)
# Apply weighting with weighting factors from file 'apparun/resources/pef30/weighting_factor.csv'
unique_score = score_init.to_unique_score(
    isNorm=True,
    isWeight=True,
    method=MethodUniqueScore.EF30,
    fileweight="apparun/resources/pef30/weighting_factor.csv",
)
print(unique_score.to_unpivoted_df())


# All functions can be applied to NodeScores obtained after impact_model.get_nodes_scores()
# Equivalent results to impact_model.get_nodes_scores() outputs with 2 scores (givent two
# different model parameters) and 5 impact categories
node_scores = [
    NodeScores(
        name="manufacturing",
        parent="ic",
        properties=NodeProperties(properties={}),
        lcia_scores=LCIAScores(
            scores={
                "EFV3_ACIDIFICATION": [0.0029179557018807847, 0.0024434297187895184],
                "EFV3_CLIMATE_CHANGE": [0.46375008402306434, 0.3774843249670958],
                "EFV3_PARTICULATE_MATTER_FORMATION": [
                    1.533898093101055e-08,
                    1.2721011456798127e-08,
                ],
                "EFV3_IONISING_RADIATION": [0.01258464933562949, 0.011859500833723233],
                "EFV3_WATER_USE": [0.18791590390291063, 0.1716230891244127],
            }
        ),
    ),
    NodeScores(
        name="use",
        parent="ic",
        properties=NodeProperties(properties={}),
        lcia_scores=LCIAScores(
            scores={
                "EFV3_ACIDIFICATION": [0.0007638828481339788, 0.0007638828481339788],
                "EFV3_CLIMATE_CHANGE": [0.10350215999388669, 0.10350215999388669],
                "EFV3_PARTICULATE_MATTER_FORMATION": [
                    6.57985314092757e-09,
                    6.57985314092757e-09,
                ],
                "EFV3_IONISING_RADIATION": [0.5950072294209235, 0.5950072294209235],
                "EFV3_WATER_USE": [0.16744676484997245, 0.16744676484997245],
            }
        ),
    ),
    NodeScores(
        name="eol",
        parent="ic",
        properties=NodeProperties(properties={}),
        lcia_scores=LCIAScores(
            scores={
                "EFV3_ACIDIFICATION": [4.7871999999999994e-08, 4.7871999999999994e-08],
                "EFV3_CLIMATE_CHANGE": [7.9288e-06, 7.9288e-06],
                "EFV3_PARTICULATE_MATTER_FORMATION": [2.3375e-13, 2.3375e-13],
                "EFV3_IONISING_RADIATION": [3.1977e-06, 3.1977e-06],
                "EFV3_WATER_USE": [9.013399999999999e-07, 9.013399999999999e-07],
            }
        ),
    ),
    NodeScores(
        name="ic",
        parent="",
        properties=NodeProperties(properties={}),
        lcia_scores=LCIAScores(
            scores={
                "EFV3_ACIDIFICATION": [0.0036818864220147635, 0.003207360438923497],
                "EFV3_CLIMATE_CHANGE": [0.567260172816951, 0.48099441376098245],
                "EFV3_PARTICULATE_MATTER_FORMATION": [
                    2.1919067821938125e-08,
                    1.93010983477257e-08,
                ],
                "EFV3_IONISING_RADIATION": [0.607595076456553, 0.6068699279546468],
                "EFV3_WATER_USE": [0.355363570092883, 0.33907075531438513],
            }
        ),
    ),
]

# If no fileweight/filenorm specified, method applied to both weighting and normalisation
# Apply default EF30 method for normalisation and weighting
unique_node_scores = [
    score_model_node.to_unique_score(isNorm=True, isWeight=True)
    for score_model_node in node_scores
]

# Convert NodeScores in DataFrame for better visualisation
unique_scores = [
    score_model_node.to_unpivoted_df() for score_model_node in unique_node_scores
]
print(pd.concat(unique_scores))
