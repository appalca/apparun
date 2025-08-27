import math
import os

import pytest
from pydantic import ValidationError

from apparun.impact_model import ImpactModel
from tests import DATA_DIR


@pytest.fixture()
def impact_model():
    return ImpactModel.from_yaml(
        os.path.join(DATA_DIR, "impact_models", "nvidia_ai_gpu_chip.yaml")
    )


def test_float_expr_invalid(impact_model):
    """
    Check an exception is raised when a float type expression is invalid.
    """
    parameters = [
        {
            "lifespan": "open('malware.txt', 'w') as file:\nfile.write('This could be a malware executable')",
        },
        {
            "cuda_core": "1 + 2 * )1 + 8(",
        },
        {
            "energy_per_inference": "custom_function(1)",
        },
    ]

    for params in parameters:
        with pytest.raises(ValidationError) as exc_info:
            impact_model.params_values(**params)

        validation_error = exc_info.value
        assert validation_error.error_count() == 1
        err = validation_error.errors()[0]
        assert err["type"] == "float_expr"
        assert err["ctx"]["target_parameter"] == list(params.keys())[0]
        assert err["input"] == list(params.values())[0]


def test_float_expr_no_such_param(impact_model):
    """
    Check an exception is raised when at least one dependency
    of a float type expr is not a parameter of the impact model.
    """
    parameters = {
        "lifespan": "cuda_core * surface",
        "cuda_core": "surface / unit_per_mm",
    }

    expected = [("surface",), ("surface", "unit_per_mm")]

    with pytest.raises(ValidationError) as exc_info:
        impact_model.params_values(**parameters)

    validation_error = exc_info.value
    assert validation_error.error_count() == 2
    errors = validation_error.errors()
    for idx, err in enumerate(errors):
        assert err["type"] == "no_such_param"
        assert err["ctx"]["target_parameter"] == list(parameters.keys())[idx]
        assert err["ctx"]["invalid_parameters"] == expected[idx]
        assert err["input"] == list(parameters.values())[idx]


def test_float_expr_dependencies_type(impact_model):
    """
    Check an exception is raised when at least one dependency of a float type expr
    is not a float type parameter.
    """
    parameters = {
        "lifespan": "usage_location * architecture",
        "cuda_core": "energy_per_inference / architecture",
    }

    expected = [("architecture", "usage_location"), ("architecture",)]

    with pytest.raises(ValidationError) as exc_info:
        impact_model.params_values(**parameters)

    validation_error = exc_info.value
    assert validation_error.error_count() == 2
    errors = validation_error.errors()
    for idx, err in enumerate(errors):
        assert err["type"] == "dependencies_type"
        assert err["ctx"]["target_parameter"] == list(parameters.keys())[idx]
        assert err["ctx"]["invalid_parameters"] == expected[idx]
        assert err["ctx"]["required_type"] == "float"
        assert err["input"] == list(parameters.values())[idx]


def test_enum_expr_no_such_param(impact_model):
    """
    Check an exception is raised when the dependency
    of an enum type expr is not a parameter of the impact model.
    """
    parameters = {
        "energy_per_inference": {"power_usage": {"Low": 0.02, "High": 0.075}},
        "architecture": {
            "usage_domain": {
                "Military": "Pascal",
                "General": "Maxwell",
            }
        },
    }

    expected = [("power_usage",), ("usage_domain",)]

    with pytest.raises(ValidationError) as exc_info:
        impact_model.params_values(**parameters)

    validation_error = exc_info.value
    assert validation_error.error_count() == 2
    errors = validation_error.errors()
    for idx, err in enumerate(errors):
        assert err["type"] == "no_such_param"
        assert err["ctx"]["target_parameter"] == list(parameters.keys())[idx]
        assert err["ctx"]["invalid_parameters"] == expected[idx]
        assert err["input"] == list(parameters.values())[idx]


def test_enum_expr_too_much_params(impact_model):
    """
    Check an exception is raised when an enum type expression
    has more than one parameter used.
    """
    parameters = {
        "lifespan": {
            "usage_location": {"FR": 1.0, "EU": 1},
            "architecture": {"Maxwell": 5, "Pascal": 4},
        },
    }

    with pytest.raises(ValidationError) as exc_info:
        impact_model.params_values(**parameters)

    validation_error = exc_info.value
    assert validation_error.error_count() == 1
    err = validation_error.errors()[0]
    assert err["type"] == "too_much_dependencies"
    assert err["ctx"]["target_parameter"] == list(parameters.keys())[0]
    assert err["ctx"]["required"] == 1
    assert err["ctx"]["value"] == 2
    assert err["input"] == list(parameters.values())[0]


def test_enum_expr_missing_options(impact_model):
    """
    Check an exception is raised when an enum type expression
    has missing options of the parameter it uses.
    """
    parameters = {
        "lifespan": {
            "usage_location": {
                "FR": 1.0,
            }
        },
    }

    with pytest.raises(ValidationError) as exc_info:
        impact_model.params_values(**parameters)

    validation_error = exc_info.value
    assert validation_error.error_count() == 1
    err = validation_error.errors()[0]
    assert err["type"] == "enum_expr_options"
    assert err["ctx"]["target_parameter"] == list(parameters.keys())[0]
    assert err["ctx"]["missing_options"] == ("EU",)
    assert err["ctx"]["extra_options"] == ()
    assert err["input"] == list(parameters.values())[0]


def test_enum_expr_invalid_options(impact_model):
    """
    Check an exception is raised when an enum type expression
    has at least one option that is not an options from the
    parameter it uses.
    """
    parameters = {
        "lifespan": {"usage_location": {"FR": 1.0, "EU": 2, "USA": -1}},
    }

    with pytest.raises(ValidationError) as exc_info:
        impact_model.params_values(**parameters)

    validation_error = exc_info.value
    assert validation_error.error_count() == 1
    err = validation_error.errors()[0]
    assert err["type"] == "enum_expr_options"
    assert err["ctx"]["target_parameter"] == list(parameters.keys())[0]
    assert err["ctx"]["missing_options"] == ()
    assert err["ctx"]["extra_options"] == ("USA",)
    assert err["input"] == list(parameters.values())[0]


def test_enum_expr_dependencies_type(impact_model):
    """
    Check an exception is raised when the parameter used
    in an enum type expression is not an enum type parameter.
    """
    parameters = {
        "lifespan": {"cuda_core": {}},
        "cuda_core": {"energy_per_inference": {}},
    }

    expected = [("cuda_core",), ("energy_per_inference",)]

    with pytest.raises(ValidationError) as exc_info:
        impact_model.params_values(**parameters)

    validation_error = exc_info.value
    assert validation_error.error_count() == 2
    errors = validation_error.errors()
    for idx, err in enumerate(errors):
        assert err["type"] == "dependencies_type"
        assert err["ctx"]["target_parameter"] == list(parameters.keys())[idx]
        assert err["ctx"]["invalid_parameters"] == expected[idx]
        assert err["ctx"]["required_type"] == "enum"
        assert err["input"] == list(parameters.values())[idx]


def test_enum_expr_missing_sub_expr(impact_model):
    """
    Check an exception is raised when an enum type expression
    has at least one option that doesn't have an associated sub
    expression.
    """
    parameters = {
        "lifespan": {"usage_location": {"EU": None, "FR": None}},
        "cuda_core": {"architecture": {"Maxwell": None, "Pascal": 15}},
    }

    expected = [
        ("EU", "FR"),
        ("Maxwell",),
    ]

    with pytest.raises(ValidationError) as exc_info:
        impact_model.params_values(**parameters)

    validation_error = exc_info.value
    assert validation_error.error_count() == 2
    errors = validation_error.errors()
    for idx, err in enumerate(errors):
        assert err["type"] == "enum_expr_empty_options"
        assert err["ctx"]["target_parameter"] == list(parameters.keys())[idx]
        assert err["ctx"]["invalid_options"] == expected[idx]
        assert err["input"] == list(parameters.values())[idx]


def test_empty_lists(impact_model):
    """
    Check  an exception is raised when at least
    one list value is empty.
    """
    parameters = {"lifespan": [], "cuda_core": []}

    expected = ["cuda_core", "lifespan"]

    with pytest.raises(ValidationError) as exc_info:
        impact_model.params_values(**parameters)

    validation_error = exc_info.value
    assert validation_error.error_count() == len(expected)
    errors = validation_error.errors()
    for err in errors:
        assert err["type"] == "empty_list"
        assert err["ctx"]["parameter"] in expected
        expected.remove(err["ctx"]["parameter"])
    assert len(expected) == 0


def test_lists_size_not_matching(impact_model):
    """
    Check an exception is raised when the list values
    don't have matching size.
    """
    parameters = {
        "lifespan": [1.0, 2.0],
        "cuda_core": [1, 5, 6, 8],
        "energy_per_inference": 1.0,
        "architecture": "Maxwell",
    }

    with pytest.raises(ValidationError) as exc_info:
        impact_model.params_values(**parameters)

    validation_error = exc_info.value
    assert validation_error.error_count() == 1
    err = validation_error.errors()[0]
    assert err["type"] == "lists_size_match"


def test_dependencies_cycles(impact_model):
    """
    Check an exception is raised when there is a cycle
    of dependencies between the expressions.
    """
    parameters = [
        {
            "architecture": {"usage_location": {"EU": "Pascal", "FR": "Maxwell"}},
            "usage_location": {"architecture": {"Maxwell": "EU", "Pascal": "FR"}},
        },
        {
            "lifespan": "log(cuda_core)",
            "cuda_core": "energy_per_inference * 100",
            "energy_per_inference": "lifespan / 10",
        },
    ]

    expected = [
        ("architecture", "usage_location"),
        ("cuda_core", "energy_per_inference", "lifespan"),
    ]

    for params, expect in zip(parameters, expected):
        with pytest.raises(ValidationError) as exc_info:
            impact_model.params_values(**params)

        errors = exc_info.value.errors()
        assert len(errors) == 1
        err = errors[0]
        assert err["type"] == "dependencies_cycle"
        assert err["ctx"]["parameters"] == expect


def test_valid_single_raw_values(impact_model):
    """
    Check no exception is raised when using valid single
    raw values.
    """
    parameters = {
        "lifespan": 1.254,
        "cuda_core": 500,
        "architecture": "Maxwell",
        "usage_location": "FR",
    }

    expected_values = {
        param.name: parameters[param.name]
        if param.name in parameters
        else param.default
        for param in impact_model.parameters
    }

    try:
        values = impact_model.params_values(**parameters)
    except Exception:
        pytest.fail("Valid values must not raise any exception")

    for name in expected_values.keys():
        if isinstance(expected_values[name], float):
            assert math.isclose(values[name][0], expected_values[name], abs_tol=1e-6)
        else:
            assert values[name][0] == expected_values[name]


def test_valid_list_raw_values(impact_model):
    """
    Check no exception is raised when using valid lists
    of raw values.
    """
    parameters = {
        "lifespan": [1.254, 1.05, 2.9999999],
        "cuda_core": [500, 461, 563],
        "architecture": "Maxwell",
        "usage_location": "FR",
    }

    expected_values = {
        **{
            param.name: [param.default] * 3
            for param in impact_model.parameters
            if param.name not in parameters
        },
        **{
            name: value if isinstance(value, list) else [value] * 3
            for name, value in parameters.items()
        },
    }

    try:
        values = impact_model.params_values(**parameters)
    except Exception:
        pytest.fail("Valid values must not raise any exception")

    for name in expected_values.keys():
        for value, expected_value in zip(values[name], expected_values[name]):
            if isinstance(value, float):
                assert math.isclose(value, expected_value, abs_tol=1e-6)
            else:
                assert value == expected_value


def test_valid_single_expr_values(impact_model):
    """
    Check no exception is raised when using valid single
    raw or expression values.
    """
    parameters = {
        "lifespan": "sqrt(cuda_core) * energy_per_inference",
        "cuda_core": {"architecture": {"Maxwell": 461, "Pascal": 520}},
        "architecture": "Maxwell",
        "energy_per_inference": {"usage_location": {"EU": 0.05, "FR": 0.02}},
    }

    expected_values = {
        **{
            param.name: param.default
            for param in impact_model.parameters
            if param.name not in parameters
        },
        **{
            "lifespan": 1.07354552768,
            "cuda_core": 461,
            "energy_per_inference": 0.05,
            "architecture": "Maxwell",
        },
    }

    try:
        values = impact_model.params_values(**parameters)
    except Exception:
        pytest.fail("Valid values must not raise any exception")

    for name in expected_values.keys():
        if isinstance(expected_values[name], float):
            assert math.isclose(values[name][0], expected_values[name], abs_tol=1e-6)
        else:
            assert values[name][0] == expected_values[name]


def test_valid_list_expr_values(impact_model):
    """
    Check no exception is raised when using valid lists
    of raw or expression values.
    """
    parameters = {
        "lifespan": [
            "(energy_per_inference ** 2) * cuda_core",
            "sin(cuda_core - 1) + energy_per_inference",
            1.41,
        ],
        "cuda_core": {"architecture": {"Maxwell": 461, "Pascal": 520}},
        "architecture": "Maxwell",
        "energy_per_inference": {"usage_location": {"EU": 0.05, "FR": 0.02}},
        "usage_location": ["EU", "EU", "FR"],
    }

    expected_values = {
        **{
            param.name: [param.default] * 3
            for param in impact_model.parameters
            if param.name not in parameters
        },
        **{
            "lifespan": [1.1525, 1.02054254665, 1.41],
            "cuda_core": [461, 461, 461],
            "energy_per_inference": [0.05, 0.05, 0.02],
            "architecture": ["Maxwell", "Maxwell", "Maxwell"],
            "usage_location": ["EU", "EU", "FR"],
        },
    }

    try:
        values = impact_model.params_values(**parameters)
    except Exception:
        pytest.fail("Valid values must not raise any exception")

    for name in expected_values.keys():
        for value, expected_value in zip(values[name], expected_values[name]):
            if isinstance(value, float):
                assert math.isclose(value, expected_value, abs_tol=1e-6)
            else:
                assert value == expected_value
