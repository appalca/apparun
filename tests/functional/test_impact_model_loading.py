"""
This module contains all the tests relative to the loading of an impact model.
"""

import os

import pytest
from pydantic import ValidationError

from apparun.impact_model import ImpactModel
from tests import DATA_DIR


def test_load_models_with_malicious_code():
    """
    Check that an exception is raised when malicious code is
    put in an impact model instead of an expression.
    """
    models_dir = os.path.join(DATA_DIR, "impact_models", "malicious_code")
    for filename in os.listdir(models_dir):
        filepath = os.path.join(models_dir, filename)
        with pytest.raises(ValidationError):
            ImpactModel.from_yaml(filepath)
            pytest.fail(
                f"An impact model with malicious code must raise an exception of type NotAnExpressionError when loaded, the model {filename} did not"
            )


def test_load_model_valid():
    """
    Check that no exception is raised when loading a valid
    impact model with no malicious code.
    """
    filepath = os.path.join(DATA_DIR, "impact_models", "nvidia_ai_gpu_chip.yaml")
    try:
        ImpactModel.from_yaml(filepath)
    except Exception:
        pytest.fail(
            "No exception should be raised when loading a valid impact model with no malicious code"
        )
