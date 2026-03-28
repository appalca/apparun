"""
This module contains the tests related to Piecewise parameters.
"""
import os

from apparun.impact_model import ImpactModel
from tests import DATA_DIR


def test_piecewise_in_parameter_value():
    """
    Assert that a model can be parameterised using Piecewise functions, including with
    dummies.
    """
    model_path = os.path.join(
        DATA_DIR, "impact_models/nvidia_ai_gpu_chip_piecewise.yaml"
    )
    model = ImpactModel.from_yaml(model_path)
    assert (
        model.get_node_scores(
            node_name="nvidia_gpu_chip_manufacturing",
            cuda_core="Piecewise((1000, architecture_Pascal), (100, True))",
            architecture="Maxwell",
        )["EFV3_CLIMATE_CHANGE"][0]
        == 0
    )
    assert (
        model.get_node_scores(
            node_name="nvidia_gpu_chip_manufacturing",
            cuda_core="Piecewise((1000, architecture_Pascal), (100, True))",
            architecture="Pascal",
        )["EFV3_CLIMATE_CHANGE"][0]
        != 0
    )
