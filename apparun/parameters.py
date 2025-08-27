from __future__ import annotations

import re
from collections import defaultdict
from typing import Dict, List, Optional, Union

import networkx as nx
import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError
from pydantic_core import PydanticCustomError
from SALib.sample import sobol

from apparun.expressions import ParamsValuesSet
from apparun.logger import logger


class ImpactModelParam(BaseModel):
    """
    Impact model parameter.
    """

    name: str
    default: Optional[Union[str, float]] = None

    def to_dict(self) -> dict:
        """
        Convert self to dict.
        :return: self as a dict
        """
        return dict(self)

    def name_is_valid(self) -> bool:
        """
        Check if parameter's name is considered as valid.
        Parameter name should only be composed of letters, numbers, underscores, and
        contain at least one letter.
        :return: if parameter's name is valid
        """
        return bool(re.match("^[A-Za-z0-9_]*$", self.name)) and bool(
            re.match("[A-Za-z]+", self.name)
        )

    @staticmethod
    def from_dict(impact_model_param: dict) -> ImpactModelParam:
        """
        Convert dict to ImpactModelParam object. Subclass must be specified in 'type'
        field.
        :param impact_model_param: dict containing construction parameters of the param.
        :return: constructed param
        """
        if impact_model_param["type"] == "float":
            param = FloatParam(**impact_model_param)
        elif impact_model_param["type"] == "enum":
            param = EnumParam(**impact_model_param)
        else:
            raise ValueError(f"Unknown parameter type {impact_model_param['type']}")
        if not param.name_is_valid():
            raise ValueError(
                f"Parameter name {param.name} is not valid. Check ImpactModelParam."
                f"name_is_valid docstring to know which name is considered valid/"
            )
        return param

    def update_default(self, new_value: Union[float, str]):
        """
        Change default value of the parameter, and compute new bounds if relevant.
        :param new_value: new default value
        """
        self.default = new_value

    def draw_to_distrib(self, samples) -> Union[List[str], List[float]]:
        return

    def corresponds(self, symbol_name: str) -> bool:
        return


class FloatParam(ImpactModelParam):
    """
    Impact model float parameter.
    Contains a default, min and max values, as well as a distribution for monte carlo
    runs.
    Supported distributions is "linear".
    """

    type: str = "float"
    min: Optional[float] = None
    max: Optional[float] = None
    distrib: Optional[str] = "linear"
    pm: Optional[float] = None
    pm_perc: Optional[float] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_bounds()

    def update_default(self, new_value: float):
        """
        Change default value of the parameter, and compute new min and max values if they
        are defined using pm or pm_perc.
        :param new_value: new default value
        """
        super().update_default(new_value)
        self.update_bounds()

    def update_bounds(self):
        """
        Compute min and max attributes from default attribute if pm, or pm_perc attributes
        is not None.
        """
        if self.default is not None:
            if self.pm is not None:
                self.min = self.default - self.pm
                self.max = self.default + self.pm
            if self.pm_perc is not None:
                self.min = self.default - (self.default * self.pm_perc)
                self.max = self.default + (self.default * self.pm_perc)

    def transform(
        self, values: Union[float, List[float]]
    ) -> Dict[str, Union[float, np.array]]:
        """
        Transform float value, or list of float values to be readily usable by
        ImpactModel.
        Value(s) are mapped to a dict with parameter name as a key.
        :param values:
        :return: a dict mapping parameter name and transformed values.
        """
        if isinstance(values, (int, float)):
            return {self.name: values}
        return {self.name: np.array(values)}

    def draw_to_distrib(self, samples: np.ndarray) -> List[float]:
        if self.distrib == "linear":
            return list(self.min + samples * (self.max - self.min))

    def corresponds(self, symbol_name: str) -> bool:
        return symbol_name == self.name


class EnumParam(ImpactModelParam):
    """
    Impact model enum parameter.
    Contains a default, list of options and associated weights for monte carlo run.
    runs.
    """

    type: str = "enum"
    weights: Dict[str, float]

    @property
    def dummies_names(self):
        """
        Give dummies names of all possible options.
        A dummy name is the option with parameter name as a prefix.
        :return: a list containing dummies names for all possible options.
        """
        return [self.full_option_name(option) for option in self.options]

    @property
    def options(self):
        return self.weights.keys()

    def update_default(self, new_value: str, weights_to_default: bool = False):
        """
        Change default value of the parameter, and optionally update the weights to match
        the new value only (which can be useful for uncertainty analysis).
        :param new_value: new default value
        :param weights_to_default: if True, the weights will be assigned to the new value
        only.
        """
        super().update_default(new_value)
        if weights_to_default:
            self.update_weights(
                {key: 1 if key == new_value else 0 for key in self.weights.keys()}
            )

    def update_weights(self, new_weights: dict[str, float]):
        """
        Change the weights of the parameter.
        :param new_weights: new weights. Keys are enum options, values are corresponding
        probability of occurrence.
        """
        self.weights = new_weights

    def full_option_name(self, option: str) -> str:
        """
        Return option with parameter name as a prefix.
        :param option: enum option.
        :return: option name with parameter name as a prefix.
        """
        return f"{self.name}_{option}"

    def look_up_table(self) -> Dict[str, Dict[str, int]]:
        """
        Map every option to its one hot encoded vector, i.e. a dict with dummies names
        and associated value (1 if corresponding to current option, 0 otherwise).
        :return: a nested dict with all option and corresponding one hot encoded vector.
        """
        return {
            option: {
                self.full_option_name(possible_option): int(option == possible_option)
                for possible_option in self.options
            }
            for option in self.options
        }

    def transform(
        self, values: Union[str, List[str]]
    ) -> Dict[str, Union[float, np.array]]:
        """
        Transform option, or list of options to be readily usable by ImpactModel.
        Value(s) one hot encoded, then mapped to a dict with parameter name as a key.
        :param values:
        :return: a dict mapping parameter name and transformed values.
        """
        if isinstance(values, list):
            return (
                pd.DataFrame([self.look_up_table().get(value) for value in values])
                .apply(np.array, axis=0, result_type="reduce")
                .to_dict()
            )
        return self.look_up_table()[values]

    def draw_to_distrib(self, samples: np.ndarray) -> List[str]:
        bin_to_names = {
            i + 1: list(self.weights.keys())[i] for i in range(len(self.weights))
        }
        weights = list(self.weights.values())
        bins = [0] + list(np.cumsum(weights) / np.sum(weights))
        transformed_samples = list(np.digitize(samples, bins))
        transformed_samples = list(
            pd.DataFrame(transformed_samples).replace(bin_to_names).values.ravel()
        )
        return transformed_samples

    def corresponds(self, symbol_name: str) -> bool:
        return symbol_name in self.dummies_names


class ImpactModelParams(BaseModel):
    parameters: List[ImpactModelParam]
    sobol_problem: Optional[Dict] = None

    @property
    def names(self):
        return [parameter.name for parameter in self.parameters]

    def to_list(self, sorted_by_name: Optional[bool] = False) -> List[Dict]:
        """
        Convert each parameter of parameters attributes to a dict, return them as a list,
        optionally sorted by parameter's name
        :param sorted_by_name: sort parameters list by parameter's name if True
        :return: list of parameter, themselves as dict
        """
        if sorted_by_name:
            sorted_names = sorted([parameter.name for parameter in self.parameters])
            return [self.get_parameter_by_name(name).to_dict() for name in sorted_names]
        return [param.to_dict() for param in self.parameters]

    def update_defaults(
        self, defaults: Dict[str, Union[str, float]], weights_to_default: bool = False
    ):
        """
        Change default value of the parameters contained in argument, and compute new
        bounds if relevant.
        :param defaults: dict containing parameter name as key and new default as
        value
        :param weights_to_default: if True, the weights of the enum parameters will be
        assigned to the new value only.
        """
        for parameter in self.parameters:
            if parameter.name in defaults.keys():
                match parameter.type:
                    case "enum":
                        parameter.update_default(
                            defaults[parameter.name], weights_to_default
                        )
                    case "float":
                        parameter.update_default(defaults[parameter.name])
                    case _:
                        raise ValueError(
                            f"Unknown ImpactModelParam type: {parameter.type}."
                        )

    def get_parameter_by_name(self, parameter_name: str) -> Optional[ImpactModelParam]:
        matching_param = [
            parameter for parameter in self if parameter.name == parameter_name
        ]
        if len(matching_param) == 0:
            return None
        return matching_param[0]

    def get_missing_parameter_names(self, parameters: Union[List, Dict]) -> List:
        known_parameters = (
            list(parameters) if isinstance(parameters, dict) else parameters
        )
        return [
            parameter for parameter in self.names if parameter not in known_parameters
        ]

    def get_default_values(self, parameter_names: List) -> Dict:
        parameters = [
            self.get_parameter_by_name(parameter_name)
            for parameter_name in parameter_names
        ]
        parameters = {parameter.name: parameter.default for parameter in parameters}
        return parameters

    def find_corresponding_parameter(
        self, symbol_name: str, must_find_one: Optional[bool] = True
    ) -> Union[ImpactModelParam, List[ImpactModelParam]]:
        matching_parameters = [
            parameter
            for parameter in self.parameters
            if parameter.corresponds(symbol_name)
        ]
        if must_find_one:
            if len(matching_parameters) > 1:
                raise ValueError(
                    f"{symbol_name} matches with multiple params ({[matching_parameter.name for matching_parameter in matching_parameters]})."
                )
            if len(matching_parameters) < 1:
                raise ValueError(f"{symbol_name} doesn't match with any params.")
            return matching_parameters[0]
        if len(matching_parameters) == 0:
            return []
        return matching_parameters

    @staticmethod
    def from_list(parameters) -> ImpactModelParams:
        return ImpactModelParams(
            parameters=[
                param
                if isinstance(param, ImpactModelParam)
                else ImpactModelParam.from_dict(param)
                for param in parameters
            ]
        )

    def __init__(self, **args):
        super().__init__(**args)
        self.__curr = 0

    def __iter__(self):
        return self

    def __next__(self) -> ImpactModelParam:
        if self.__curr >= len(self.parameters):
            self.__curr = 0
            raise StopIteration()

        param = self.parameters[self.__curr]
        self.__curr += 1
        return param

    def __getitem__(self, key: int | str) -> ImpactModelParam:
        if isinstance(key, int):
            return self.parameters[key]
        else:
            return self.get_parameter_by_name(key)

    def set_sobol_problem(self):
        self.sobol_problem = {
            "num_vars": len(self.parameters),
            "names": [parameter.name for parameter in self.parameters],
            "bounds": [[0, 1]] * len(self.parameters),
        }

    def sobol_draw(self, n) -> np.ndarray:
        self.set_sobol_problem()
        samples = sobol.sample(self.sobol_problem, n)
        return samples

    def uniform_draw(self, n) -> np.ndarray:
        return np.random.rand(n, len(self.parameters))

    def draw_to_distrib(
        self, samples: np.ndarray
    ) -> Dict[str, Union[List[float], List[str]]]:
        return {
            self.parameters[i].name: self.parameters[i].draw_to_distrib(samples[:, i])
            for i in range(len(self.parameters))
        }


class ImpactModelParamsValues(BaseModel):
    """
    A set of values for the parameters of an impact model.

    ATTENTION!! Use the method from dict to build instance of this class.
    """

    values: Dict[str, List[Union[float, int, str]]]

    def __getitem__(self, item):
        if item in self.values.keys():
            return self.values[item]
        else:
            raise KeyError()

    @classmethod
    def from_dict(
        cls,
        parameters: ImpactModelParams,
        values: Dict[
            str, Union[float, int, str, dict, List[Union[float, int, str, dict]]]
        ],
    ) -> ImpactModelParamsValues:
        # Values with the default values for the parameters not in the values
        all_values = {
            **values,
            **{
                param.name: param.default
                for param in parameters
                if param.name not in values
            },
        }
        # Step 1 - Transform all values into lists
        empty_list_values = [
            name
            for name, value in values.items()
            if isinstance(value, list) and len(value) == 0
        ]
        if empty_list_values:
            raise ValidationError.from_exception_data(
                "",
                line_errors=[
                    {
                        "loc": ("values",),
                        "msg": "",
                        "type": PydanticCustomError(
                            "empty_list",
                            "The value for the parameter {parameter} can't be an empty list",
                            {"parameter": name},
                        ),
                    }
                    for name in empty_list_values
                ],
            )

        list_values = [value for value in values.values() if isinstance(value, list)]
        if any(
            len(list_values[0]) != len(list_values[i])
            for i in range(1, len(list_values))
        ):
            raise ValidationError.from_exception_data(
                "",
                line_errors=[
                    {
                        "loc": ("values",),
                        "msg": "",
                        "type": PydanticCustomError(
                            "lists_size_match", "List values must have matching sizes"
                        ),
                    }
                ],
            )

        size = max(map(len, list_values)) if list_values else 1
        list_values = {
            name: value if isinstance(value, list) else [value] * size
            for name, value in all_values.items()
        }

        # Step 2 - Transform the values to expressions
        exprs_sets = []
        for idx in range(size):
            exprs_sets.append(
                ParamsValuesSet.build(
                    {name: value[idx] for name, value in list_values.items()},
                    parameters,
                )
            )

        # Step 3 - Dependencies cycles detection
        for exprs_set in exprs_sets:
            try:
                cycle = exprs_set.dependencies_cycle()
                if cycle:
                    raise ValidationError.from_exception_data(
                        "",
                        line_errors=[
                            {
                                "loc": ("values",),
                                "msg": "",
                                "type": PydanticCustomError(
                                    "dependencies_cycle",
                                    "The expressions for the parameters {parameters} are inter-dependent",
                                    {"parameters": tuple(sorted(cycle))},
                                ),
                            }
                        ],
                    )
            except nx.NetworkXNoCycle:
                pass

        # Step 4 - Expressions' evaluation
        final_values = defaultdict(list)
        for exprs_set in exprs_sets:
            evals = exprs_set.evaluate()
            for name, value in evals.items():
                final_values[name].append(value)

        # Step 5 - Validation of the final values
        errors = []
        for name, value in final_values.items():
            for idx, elem in enumerate(value):
                parameter = parameters[name]
                match parameter.type:
                    case "float" if elem < parameter.min or elem > parameter.max:
                        if exprs_sets[idx][name].is_complex:
                            logger.warning(
                                "The value %s (got after evaluating the expression %s) for the parameter %s is outside its [min, max] range",
                                str(elem),
                                name,
                                str(exprs_sets[idx][name].raw_version),
                            )
                        else:
                            logger.warning(
                                "The value %s for the parameter %s is outside its [min, max] range",
                                str(elem),
                                name,
                            )
                    case "enum" if elem not in parameter.options:
                        if exprs_sets[idx][name].is_complex:
                            errors.append(
                                {
                                    "type": PydanticCustomError(
                                        "value_error",
                                        "Invalid value {value}, got after evaluating the expression {expr}, for the parameter {target_parameter}",
                                        {
                                            "value": elem,
                                            "target_parameter": name,
                                            "expr": str(
                                                exprs_sets[idx][name].raw_version
                                            ),
                                        },
                                    )
                                }
                            )
                        else:
                            errors.append(
                                {
                                    "type": PydanticCustomError(
                                        "value_error",
                                        "Invalid value {value} for the parameter {target_parameter}",
                                        {"value": elem, "target_parameter": name},
                                    )
                                }
                            )
        if errors:
            raise ValidationError.from_exception_data("", line_errors=errors)

        return ImpactModelParamsValues(**{"values": final_values})

    def items(self):
        return self.values.items()
