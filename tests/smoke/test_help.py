"""
This module contain the tests to check that the option --help of the commands works.
"""

import subprocess

from typer.testing import CliRunner

from apparun.cli.main import cli_app

runner = CliRunner()


def test_help():
    result = runner.invoke(cli_app, ["--help"])
    assert result.exit_code == 0


def test_compute_help():
    result = runner.invoke(cli_app, ["compute", "--help"])
    assert result.exit_code == 0


def test_compute_nodes_help():
    result = runner.invoke(cli_app, ["compute-nodes", "--help"])
    assert result.exit_code == 0


def test_models_help():
    result = runner.invoke(cli_app, ["models", "--help"])
    assert result.exit_code == 0


def test_models_params_help():
    result = runner.invoke(cli_app, ["model-params", "--help"])
    assert result.exit_code == 0


def test_results_help():
    result = runner.invoke(cli_app, ["results", "--help"])
    assert result.exit_code == 0
