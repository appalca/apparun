from typing import Literal

import pandas as pd
import streamlit as st
import yaml

from apparun.cli.main import generate_gui
from apparun.gui.panels.base import (
    ACTION_ADD,
    InputScenarioFormPanel,
    StaticOutputPanel,
    register_panel,
)
from apparun.gui.panels.output_dynamic import ScenarioComparisonDynamicOutputPanel
from apparun.impact_model import ImpactModel


@register_panel("polite_markdown")
class PoliteMarkdown(StaticOutputPanel):
    type: Literal["polite_markdown"]
    message: str

    def run(self):
        st.markdown(f"{self.message}\n\nKind regards.")


@register_panel("batch_scenario_comparison_dynamic_output_panel")
class BatchScenarioComparisonDynamicOutputPanel(ScenarioComparisonDynamicOutputPanel):
    type: Literal["batch_scenario_comparison_dynamic_output_panel"]

    def __init__(self, **args):
        super().__init__(**args)
        self._state["scenarios"] = {}

    def run(
        self,
        entry_data,
        impact_model: ImpactModel = None,
        lca_data: pd.DataFrame = None,
    ):
        if entry_data["action"] == ACTION_ADD:
            scenario_scores = self.get_results(
                entry_data["parameters"], impact_model, lca_data
            )
            fig = self.result.get_figure(scenario_scores)
            st.plotly_chart(fig)


@register_panel("input_scenario_from_file_panel")
class ScenarioFromFilePanel(InputScenarioFormPanel):
    type: Literal["input_scenario_from_file_panel"]

    def run(self):
        self.st_component = st.form(self._uuid)

        if self.name is not None:
            self.st_component.markdown(f"### {self.name}")

        uploaded_files = self.st_component.file_uploader(
            "Upload parameters", accept_multiple_files="directory", type="yaml"
        )
        for uploaded_file in uploaded_files:
            scenario_name = uploaded_file.name.split("/")[-1].split(".")[:-1][0]
            self._state["parameters"][scenario_name] = yaml.safe_load(
                uploaded_file.getvalue()
            )

        scenarios_add = self.st_component.form_submit_button("Compute")

        if scenarios_add and len(uploaded_files) > 0:
            self._state["action"] = ACTION_ADD


generate_gui("samples/conf/custom_gui.yaml")
