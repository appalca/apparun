import uuid
from typing import Any, Callable, Dict, List, Literal, Optional

import pandas as pd
import streamlit as st
from pydantic import BaseModel

from apparun.impact_model import ImpactModel
from apparun.results import ImpactModelResult

ACTION_ADD = "add"
ACTION_CLEAR = "clear"

INPUT_PANELS = {}
OUTPUT_PANELS = {}


def register_panel(panel_type: str):
    """
    This decorator registers a new Panel class in PANELS registry.
    :param panel_type: new Panel's type name
    :return: new Panel class
    """

    def decorator(decorated_class):
        if issubclass(decorated_class, OutputPanel):
            if panel_type not in OUTPUT_PANELS:
                OUTPUT_PANELS[panel_type] = decorated_class
            return decorated_class
        if issubclass(decorated_class, InputPanel):
            if panel_type not in INPUT_PANELS:
                INPUT_PANELS[panel_type] = decorated_class
            return decorated_class
        msg = f"Custom panel {panel_type} must inherit from InputPanel or OutputPanel."
        raise TypeError(msg)

    return decorator


def get_input_panel(panel_type: str):
    """
    Get a registered InputPanel class by type.
    :param panel_type: type of the desired input panel.
    :return: registered InputPanel class corresponding to the type.
    """
    return INPUT_PANELS[panel_type]


def get_output_panel(panel_type: str):
    """
    Get a registered OutputPanel class by type.
    :param panel_type: type of the desired output panel.
    :return: registered OutputPanel class corresponding to the type.
    """
    return OUTPUT_PANELS[panel_type]


def registered_input_panels() -> List[str]:
    """
    Get a list of registered InputPanel types.
    :return: list of registered InputPanel types.
    """
    return list(INPUT_PANELS.keys())


def registered_output_panels() -> List[str]:
    """
    Get a list of registered OutputPanel types.
    :return: list of registered OutputPanel types.
    """
    return list(OUTPUT_PANELS.keys())


class Panel(BaseModel):
    _state: Dict[Any, Any] = {}

    st_component: Callable = None

    def spawn(self):
        return

    @property
    def state(self):
        return self._state


class OutputPanel(Panel):
    type: Literal["output_panel"]

    def run(self, **args):
        return


class DynamicOutputPanel(OutputPanel):
    type: Literal["dynamic_output_panel"]
    result: Optional[ImpactModelResult] = None

    def compute_from_impact_model(self, entry_data, impact_model):
        return

    def fetch_from_lca_data(self, entry_data, lca_data):
        return

    def get_results(
        self,
        entry_data,
        impact_model: ImpactModel = None,
        lca_data: pd.DataFrame = None,
    ):
        if impact_model is not None:
            return self.compute_from_impact_model(entry_data, impact_model)
        if lca_data is not None:
            return self.fetch_from_lca_data(entry_data, lca_data)
        raise ValueError(
            "Cannot get module results: no impact model nor lca data are provided."
        )


class StaticOutputPanel(OutputPanel):
    type: Literal["static_output_panel"]

    def run(self):
        return


class InputPanel(Panel):
    name: Optional[str] = None
    _uuid: Optional[str] = None

    def __init__(self, **args):
        super().__init__(**args)
        self._uuid = uuid.uuid4().hex

    def submit(self):
        return


@register_panel("input_scenario_form_panel")
class InputScenarioFormPanel(InputPanel):
    fields: Optional[List[Dict[str, Any]]] = []
    type: Literal["input_scenario_form_panel"]

    def __init__(self, **args):
        super().__init__(**args)
        self._state["parameters"] = {}
        self._state["action"] = None

    def run(self):
        self.st_component = st.form(self._uuid)

        if self.name is not None:
            self.st_component.markdown(f"### {self.name}")

        self._state["scenario_name"] = self.st_component.text_input(
            label="Scenario name"
        )
        for input_field in self.fields:
            if input_field["type"] == "float":
                self._state["parameters"][
                    input_field["name"]
                ] = self.st_component.text_input(
                    label=input_field["name"], value=input_field["default"]
                )
            if input_field["type"] == "enum":
                self._state["parameters"][
                    input_field["name"]
                ] = self.st_component.selectbox(
                    label=input_field["name"], options=input_field["options"]
                )
        col_button1, col_button2 = st.columns(2)
        with col_button1:
            scenarios_add = self.st_component.form_submit_button("Add")
        with col_button2:
            scenarios_clear = self.st_component.form_submit_button("Clear")
        if scenarios_add:
            self._state["action"] = ACTION_ADD
        if scenarios_clear:
            self._state["action"] = ACTION_CLEAR
