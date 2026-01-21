import math

import pytest

from apparun.exceptions import InvalidFileError
from apparun.impact_methods import MethodFullName, MethodShortName, MethodUniqueScore
from apparun.impact_model import ImpactModel


@pytest.fixture()
def impact_model_16():
    return ImpactModel.from_yaml("tests/data/impact_models/multi_indicator_model.yaml")


@pytest.fixture()
def impact_model_5():
    return ImpactModel.from_yaml("tests/data/impact_models/5_indicator_model.yaml")


@pytest.fixture()
def impact_model_5_ef31():
    return ImpactModel.from_yaml("tests/data/impact_models/5_indicator_model_ef31.yaml")


def test_unique_score_exception(impact_model_16):
    """
    Check an exception is raised when impact categories from normalisation
    or weighting file are not matching model impact categories.
    """
    with pytest.raises(InvalidFileError):
        impact_model_16.get_scores().to_normalised(
            filenorm="tests/data/norm_w_factors/invalid/error_number_factor.csv"
        )

    with pytest.raises(InvalidFileError):
        impact_model_16.get_scores().to_normalised(
            filenorm="tests/data/norm_w_factors/invalid/error_typo_pef_factor.csv"
        )

    with pytest.raises(InvalidFileError):
        impact_model_16.get_scores().to_weighted(
            fileweight="tests/data/norm_w_factors/invalid/error_number_factor.csv"
        )

    with pytest.raises(InvalidFileError):
        impact_model_16.get_scores().to_weighted(
            fileweight="tests/data/norm_w_factors/invalid/error_typo_pef_factor.csv"
        )

    with pytest.raises(InvalidFileError):
        impact_model_16.get_scores().to_unique_score(
            is_normalised=True,
            filenorm="tests/data/norm_w_factors/invalid/error_number_factor.csv",
        )

    with pytest.raises(InvalidFileError):
        impact_model_16.get_scores().to_unique_score(
            is_normalised=True,
            filenorm="tests/data/norm_w_factors/invalid/error_typo_pef_factor.csv",
        )


def test_unique_score_values(impact_model_5, impact_model_5_ef31):
    try:
        score_30 = impact_model_5.get_scores().to_unique_score(
            method=MethodUniqueScore.EF30, is_normalised=True, is_weighted=True
        )
    except Exception:
        pytest.fail(
            "Valid factors / reduced number of impact cat. in model must not raise any exception"
        )
    try:
        score_31 = impact_model_5_ef31.get_scores().to_unique_score(
            method=MethodUniqueScore.EF31, is_normalised=True, is_weighted=True
        )
    except Exception:
        pytest.fail(
            "Valid factors / reduced number of impact cat. in model must not raise any exception"
        )
    assert math.isclose(
        score_30.scores.get("UNIQUE_SCORE")[0], 0.00361857, abs_tol=1e-6
    )
    assert math.isclose(
        score_31.scores.get("UNIQUE_SCORE")[0], 0.00344846, abs_tol=1e-6
    )


def test_unique_score_values_multi_param(impact_model_5):
    try:
        score = impact_model_5.get_scores(test_param=[1, 2]).to_unique_score(
            is_normalised=True, is_weighted=True
        )
    except Exception:
        pytest.fail(
            "Valid factors / reduced number of impact cat. in model must not raise any exception"
        )

    assert len(score.scores.get("UNIQUE_SCORE")) == 2
    assert math.isclose(score.scores.get("UNIQUE_SCORE")[0], 0.00361857, abs_tol=1e-6)
    assert math.isclose(score.scores.get("UNIQUE_SCORE")[1], 0.00361857, abs_tol=1e-6)
    # assert score.scores.get("UNIQUE_SCORE") == [0.013462, 0.012886]


def test_unique_node_score_values(impact_model_5):
    node_scores = impact_model_5.get_nodes_scores()
    try:
        unique_node_scores = [
            node_score.to_unique_score(is_normalised=True, is_weighted=True)
            for node_score in node_scores
        ]
    except Exception:
        pytest.fail(
            "Valid factors / reduced number of impact cat. in model must not raise any exception"
        )

    assert math.isclose(
        unique_node_scores[0].lcia_scores.scores.get("UNIQUE_SCORE")[0],
        0.00361857,
        abs_tol=1e-6,
    )
    assert math.isclose(
        unique_node_scores[1].lcia_scores.scores.get("UNIQUE_SCORE")[0],
        0.00361857,
        abs_tol=1e-6,
    )
    assert math.isclose(
        unique_node_scores[2].lcia_scores.scores.get("UNIQUE_SCORE")[0],
        0.00361857,
        abs_tol=1e-6,
    )
    assert math.isclose(
        unique_node_scores[3].lcia_scores.scores.get("UNIQUE_SCORE")[0],
        0.00361857,
        abs_tol=1e-6,
    )


def test_unique_node_score_values_multi_param(impact_model_5):
    node_scores = impact_model_5.get_nodes_scores(test_param=[1, 2])
    try:
        unique_node_scores = [
            node_score.to_unique_score(is_normalised=True, is_weighted=True)
            for node_score in node_scores
        ]
    except Exception:
        pytest.fail(
            "Valid factors / reduced number of impact cat. in model must not raise any exception"
        )

    assert len(unique_node_scores[0].lcia_scores.scores.get("UNIQUE_SCORE")) == 2
    assert math.isclose(
        unique_node_scores[0].lcia_scores.scores.get("UNIQUE_SCORE")[0],
        0.00361857,
        abs_tol=1e-6,
    )
    assert math.isclose(
        unique_node_scores[1].lcia_scores.scores.get("UNIQUE_SCORE")[1],
        0.00361857,
        abs_tol=1e-6,
    )
    assert math.isclose(
        unique_node_scores[2].lcia_scores.scores.get("UNIQUE_SCORE")[0],
        0.00361857,
        abs_tol=1e-6,
    )
    assert math.isclose(
        unique_node_scores[3].lcia_scores.scores.get("UNIQUE_SCORE")[1],
        0.00361857,
        abs_tol=1e-6,
    )


def test_impact_methods_consistency():
    assert {elem.name for elem in MethodFullName} == {
        elem.name for elem in MethodShortName
    }
