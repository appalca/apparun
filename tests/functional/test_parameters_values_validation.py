"""
This module contains the tests for the validation of the values of the parameters of an impact model.
"""

import os

import numpy as np
import pytest

from apparun.impact_model import ImpactModel
from tests import DATA_DIR

impact_model_path = os.path.join(
    os.environ["APPARUN_IMPACT_MODELS_DIR"], "nvidia_ai_gpu_chip.yaml"
)


def test_float_invalid_value_type():
    """
    Check an exception is raised when the value used to initialize an impact model
    parameter of type float is not a valids type.
    """
    impact_model = ImpactModel.from_yaml(impact_model_path)

    # Test with a single value
    params = {"cuda_core": "low"}
    try:
        impact_model.validate_parameters_values(params)
        pytest.fail(
            "Impossible to assign a value of different type of its target parameter"
        )
    except TypeError:
        pass

    # Test with a list of values
    params = {"cuda_core": [125, "low"]}
    try:
        impact_model.validate_parameters_values(params)
        pytest.fail(
            "Impossible to assign a value of different type of its target parameter"
        )
    except TypeError:
        pass


def test_enum_invalid_value_type():
    """
    Check an exception is raised when the value used to initialize an impact model
    parameter of type enum is not a valids type.
    """
    impact_model = ImpactModel.from_yaml(impact_model_path)

    # Test with a single value
    params = {"architecture": 12.0}
    try:
        impact_model.validate_parameters_values(params)
        pytest.fail("Impossible to assign a float value to a enum type parameter")
    except TypeError:
        pass

    # Test with a list of values
    params = {"architecture": ["Maxwell", 124.45, "Pascal"]}
    try:
        impact_model.validate_parameters_values(params)
        pytest.fail("Impossible to assign a float value to a enum type parameter")
    except TypeError:
        pass


def test_lists_not_equal_sizes():
    """
    Check an exception is raised when two parameters are given as lists
    but the lists are not the same size.
    """
    impact_model = ImpactModel.from_yaml(impact_model_path)

    params = {"cuda_core": [1.0, 25.0, 120.0], "lifespan": [1.5, 30.0]}

    try:
        impact_model.validate_parameters_values(params)
        pytest.fail("All list parameters must have matching size")
    except ValueError:
        pass


def test_lists_empty():
    """
    Check an exception is raised when parameters are given as lists
    but the lists are empty.
    """
    impact_model = ImpactModel.from_yaml(impact_model_path)

    params = {"cuda_core": [], "lifespan": []}

    try:
        impact_model.validate_parameters_values(params)
        pytest.fail("All list parameters cannot be empty")
    except ValueError:
        pass


def test_enum_not_an_option():
    """
    Check an exception is raised when a value given to a parameter of type enum
    is not one the possible options for this parameter.
    """
    impact_model = ImpactModel.from_yaml(impact_model_path)

    # Test with a single value
    params = {"architecture": "Lovelace"}
    try:
        impact_model.validate_parameters_values(params)
        pytest.fail(
            "Impossible to assign a value for a enum type parameter that is not one of the possible options"
        )
    except ValueError:
        pass

    # Test with a list with only one invalid value
    params = {"architecture": ["Pascal", "Lovelace", "Maxwell"]}
    try:
        impact_model.validate_parameters_values(params)
        pytest.fail(
            "Impossible to assign a value for a enum type parameter that is not one of the possible options"
        )
    except ValueError:
        pass


def test_float_valid():
    """
    Check no exception is raised when given valid values for a float type parameter.
    """
    impact_model = ImpactModel.from_yaml(impact_model_path)

    # Test with a single value
    params = {"lifespan": [1.2, 2, np.float16(2.4), np.int32(3)]}

    try:
        impact_model.validate_parameters_values(params)
    except Exception:
        pytest.fail("No exception should be raised for valid values")
