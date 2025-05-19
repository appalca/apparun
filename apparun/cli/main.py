import os
from typing import Optional

import typer
import yaml
from yaml import YAMLError

import apparun.core
from apparun.logger import logger

cli_app = typer.Typer()


def load_yaml(filepath, mode):
    try:
        with open(filepath, mode) as stream:
            return yaml.safe_load(stream)
    except FileNotFoundError:
        logger.error("No such file: %s", filepath)
        raise
    except YAMLError:
        logger.error("Invalid yaml file: %s", filepath)
        raise


@cli_app.command()
def compute(
    impact_model_name: str,
    params_file_path: str,
    output_file_path: Optional[str] = None,
):
    try:
        logger.info("Command compute begin")
        logger.info("Loading parameters values")
        params = load_yaml(params_file_path, "r") or {}
        logger.info("Parameters values loaded with no error")

        scores = apparun.core.compute_impacts(impact_model_name, params)
        if output_file_path is not None:
            with open(output_file_path, "w") as stream:
                yaml.dump(scores, stream, sort_keys=False)
            logger.info("FU impact scores saved at the path: %s", output_file_path)
        logger.info("Command compute finished with no error")
    except Exception:
        exit(1)


@cli_app.command()
def compute_nodes(
    impact_model_name: str,
    params_file_path: str,
    output_file_path: Optional[str] = None,
):
    try:
        logger.info("Command compute-nodes begin")
        logger.info("Loading parameters values")
        params = load_yaml(params_file_path, "r") or {}
        logger.info("Parameters values loaded with no error")

        scores = apparun.core.compute_impacts(impact_model_name, params, all_nodes=True)
        print(scores)
        if output_file_path is not None:
            with open(output_file_path, "w") as stream:
                yaml.dump(scores, stream, sort_keys=False)
            logger.info("Nodes scores saved at the path: %s", output_file_path)
        logger.info("Command compute-nodes finished with no error")
    except Exception:
        exit(1)


@cli_app.command()
def models():
    try:
        logger.info("Command models begin")
        valid_impact_models = apparun.core.get_valid_models()
        print(valid_impact_models)
        logger.info("Command models finished with no error")
    except Exception:
        exit(1)


@cli_app.command()
def model_params(impact_model_name: str):
    try:
        logger.info("Command model-params begin")
        impact_model_params = apparun.core.get_model_params(impact_model_name)
        print(impact_model_params)
        logger.info("Command models finished with no error")
    except Exception:
        exit(1)


@cli_app.command()
def results(results_config_file_path: str):
    try:
        logger.info("Command results begin")
        results_config = load_yaml(results_config_file_path, "r")
        apparun.core.compute_results(results_config)
        logger.info("Command results finished with no error")
    except FileNotFoundError:
        logger.error(f"No such file: {results_config_file_path}")
        exit(1)
    except Exception:
        exit(1)


if __name__ == "__main__":
    cli_app()
