import os
from typing import Optional

import typer
import yaml

import apparun.core

cli_app = typer.Typer()


@cli_app.command()
def compute(
    impact_model_name: str,
    params_file_path: str,
    output_file_path: Optional[str] = None,
):
    with open(params_file_path, "r") as stream:
        params = yaml.safe_load(stream) or {}
    scores = apparun.core.compute_impacts(impact_model_name, params)
    print(scores)
    if output_file_path is not None:
        with open(output_file_path, "w") as stream:
            yaml.dump(scores, stream, sort_keys=False)


@cli_app.command()
def compute_nodes(
    impact_model_name: str,
    params_file_path: str,
    output_file_path: Optional[str] = None,
):
    with open(params_file_path, "r") as stream:
        params = yaml.safe_load(stream) or {}
    scores = apparun.core.compute_impacts(impact_model_name, params, all_nodes=True)
    print(scores)
    if output_file_path is not None:
        with open(output_file_path, "w") as stream:
            yaml.dump(scores, stream, sort_keys=False)


@cli_app.command()
def models():
    valid_impact_models = apparun.core.get_valid_models()
    print(valid_impact_models)


@cli_app.command()
def model_params(impact_model_name: str):
    impact_model_params = apparun.core.get_model_params(impact_model_name)
    print(impact_model_params)


@cli_app.command()
def results(results_config_file_path: str):
    with open(results_config_file_path, "r") as stream:
        results_config = yaml.safe_load(stream)
    apparun.core.compute_results(results_config)


if __name__ == "__main__":
    cli_app()
