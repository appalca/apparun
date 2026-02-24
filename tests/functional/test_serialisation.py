import os

import pytest

from apparun.impact_model import ImpactModel, ModelMetadata
from tests import DATA_DIR


@pytest.fixture()
def impact_model():
    return ImpactModel.from_yaml(
        os.path.join(DATA_DIR, "impact_models", "nvidia_ai_gpu_chip.yaml")
    )


def test_default_metadata(impact_model):
    default_metadata = ModelMetadata()
    impact_model.metadata = default_metadata
    new_impact_model = impact_model.to_dict()
    new_impact_model = ImpactModel.from_dict(new_impact_model)
    assert default_metadata == new_impact_model.metadata


def test_serialisation_deserialisation_scores(impact_model):
    initial_scores = impact_model.get_nodes_scores()
    new_impact_model = ImpactModel.from_dict(impact_model.to_dict())
    scores = new_impact_model.get_nodes_scores()
    assert scores == pytest.approx(initial_scores)

    new_model_filename = "model_serialised.yaml"

    impact_model.to_yaml(new_model_filename)
    yaml_impact_model = ImpactModel.from_yaml(new_model_filename)
    scores = yaml_impact_model.get_nodes_scores()
    assert scores == pytest.approx(initial_scores)

    os.remove(new_model_filename)
