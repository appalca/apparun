import os

import pytest

from apparun.impact_methods import MethodFullName, MethodShortName
from apparun.impact_model import ImpactModel, ModelMetadata
from apparun.impact_tree import ImpactTreeNode
from apparun.parameters import ImpactModelParams
from apparun.results import get_result


def test_impact_tree_calculation():
    impact_model = ImpactModel().from_yaml("data/noparam_system.yaml")
    lcia_scores = impact_model.get_scores()
    scores = sorted(lcia_scores.scores.items())
    assert dict(scores) == {'EFV3_CLIMATE_CHANGE': 1.3830513221576728e-06, 'EFV3_ECOTOXICITY_FRESHWATER': 4.365302017373894e-12, 'EFV3_LAND_USE': 0.0}

def test_impact_calculation_result():
    impact_model = ImpactModel().from_yaml("data/noparam_system.yaml")
    lcia_nodes_scores = impact_model.get_nodes_scores()

    print(lcia_nodes_scores)

    tree_result = get_result("tree_map")(
        impact_model=impact_model,
        n=4096,
        output_name="treemap",
        pdf_save_path=os.path.join("outputs", "figures/"),
        table_save_path=os.path.join("outputs", "tables/"),
        html_save_path=os.path.join("outputs", "figures/"),
    )

    result_table = tree_result.get_table()
    tree_result.get_figure(result_table)
    assert os.path.exists("outputs/tables/treemap.csv")
    assert os.path.exists("outputs/figures/treemap-EFV3_CLIMATE_CHANGE.pdf")
    assert os.path.exists("outputs/figures/treemap-EFV3_CLIMATE_CHANGE.html")
