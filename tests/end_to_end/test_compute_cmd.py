"""
This module contains the tests related to the compute command.
"""

import os

from typer.testing import CliRunner

from apparun.cli.main import cli_app
from tests import DATA_DIR

runner = CliRunner()


def test_parameters_file_not_found():
    """
    Check that the command fails when the file of the parameters can't be found.
    The exit code must be 1.
    """
    parameters_path = os.path.join(
        DATA_DIR, "parameters", "invalids", "non_existing_parameters.yaml"
    )
    result = runner.invoke(cli_app, ["compute", "nvidia_gpu_chip", parameters_path])
    assert result.exit_code == 1


def test_parameters_invalid_yaml_file():
    """
    Check that the command fails when the file of the parameters is not a valid yaml file.
    The exit code must be 1.
    """
    parameters_path = os.path.join(
        DATA_DIR, "parameters", "invalids", "invalid_yaml_parameters.yaml"
    )
    result = runner.invoke(cli_app, ["compute", "nvidia_gpu_chip", parameters_path])
    assert result.exit_code == 1


def test_valid_no_exception():
    """
    Check that a valid command call doesn't raise any exception and exit with an exit code of 0.
    """
    parameters_path = os.path.join(
        DATA_DIR, "parameters", "valids", "valid_parameters.yaml"
    )
    result = runner.invoke(cli_app, ["compute", "nvidia_ai_gpu_chip", parameters_path])
    assert result.exit_code == 0
