import os
import time
from functools import wraps
from typing import Dict, List, Union

from apparun import results
from apparun.impact_model import ImpactModel
from apparun.logger import logger
from apparun.results import get_result

IMPACTS_MODEL_DIR = os.environ.get("APPARUN_IMPACT_MODELS_DIR")
if IMPACTS_MODEL_DIR is None:
    logger.error("Environment variable IMPACTS_MODEL_DIR is undefined")
    exit(1)


def execution_time_logging(func):
    """
    Decorator to log execution time as an info.
    :param func: function to wrap.
    :return: wrapped function.
    """

    @wraps(func)
    def execution_time_logging_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        logger.info(f"Function {func.__name__} executed in {total_time:.4f} seconds")
        return result

    return execution_time_logging_wrapper


@execution_time_logging
def compute_impacts(
    impact_model_name: str, params: Dict, all_nodes: bool = False
) -> Union[List, Dict[str, Union[float, List[float]]]]:
    """
    Load an impact model from disk from its name, and get impact scores of the root node
    for each impact method, according to the parameters.
    APPARUN_IMPACT_MODELS_DIR environment variable should be specified (see README.md).
    :param impact_model_name: name of the impact model to load
    :param params: value, or list of values of the impact model's parameters.
    List of values must have the same length. If single values are provided
    alongside a list of values, it will be duplicated to the appropriate length.
    :param all_nodes: if True, scores will be computed for each node. Only root node
    otherwise (default).
    :return: a dict mapping impact names and corresponding score, or list of scores.
    """
    impact_model = ImpactModel.from_yaml(
        os.path.join(IMPACTS_MODEL_DIR, f"{impact_model_name}.yaml")
    )
    if all_nodes:
        return impact_model.get_nodes_scores(**params)
    return dict(impact_model.get_scores(**params))


@execution_time_logging
def get_valid_models() -> List[str]:
    """
    Get a list of all valid impact models in the directory specified by
    APPARUN_IMPACT_MODELS_DIR environment variable.
    :return: a list of all valid impact models.
    """
    valid_impact_models = []
    for file in os.listdir(IMPACTS_MODEL_DIR):
        if file.endswith(".yaml"):
            try:
                ImpactModel.from_yaml(os.path.join(IMPACTS_MODEL_DIR, file))
                valid_impact_models.append(file.replace(".yaml", ""))
            except KeyError:
                logger.error(
                    f"{file.replace('.yaml', '')} is not a valid impact model."
                )
    return valid_impact_models


@execution_time_logging
def get_model_params(impact_model_name: str) -> List[Dict]:
    """
    Return the list of parameters required to execute an impact model.
    APPARUN_IMPACT_MODELS_DIR environment variable should be specified (see README.md).
    :param impact_model_name: name of the impact model to load.
    :return: a list of parameters required by the model.
    """
    impact_model = ImpactModel.from_yaml(
        os.path.join(IMPACTS_MODEL_DIR, f"{impact_model_name}.yaml")
    )
    return [parameter.to_dict() for parameter in impact_model.parameters]


@execution_time_logging
def compute_results(results_config: List[Dict]):
    """
    Generate results according to results_config.
    :param results_config: list of results wanted. Each element of this list will be
    used to construct an ImpactModelResult, using the elements in "args" argument.
    Result subclass is determined by "class" argument.
    """
    for result_config in results_config:
        result_name = result_config["result_name"]
        result_constructor_args = result_config["args"]
        if "parameters" in result_constructor_args["impact_model"]:
            result_constructor_args["parameters"] = result_constructor_args[
                "impact_model"
            ]["parameters"]
        result_constructor_args["impact_model"] = ImpactModel.from_yaml(
            os.path.join(
                IMPACTS_MODEL_DIR,
                f"{result_constructor_args['impact_model']['name']}.yaml",
            )
        )
        result_class = get_result(result_name)
        result_objet = result_class(**result_constructor_args)
        result_objet.run()
