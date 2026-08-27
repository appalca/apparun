from typing import Literal, Optional

import pandas as pd
import streamlit as st

from apparun.gui.panels.base import (
    ACTION_ADD,
    ACTION_CLEAR,
    DynamicOutputPanel,
    register_panel,
)
from apparun.impact_model import ImpactModel
from apparun.results import HeatmapResult, ImpactModelResult, ScenarioComparisonResult


@register_panel("scenario_comparison_dynamic_output_panel")
class ScenarioComparisonDynamicOutputPanel(DynamicOutputPanel):
    type: Literal["scenario_comparison_dynamic_output_panel"]
    result: Optional[ImpactModelResult] = None
    y: str
    hue: str
    by_property: Optional[str] = None

    def __init__(self, **args):
        super().__init__(**args)
        self._state["scenario_parameters"] = {}

    def compute_from_impact_model(self, entry_data, impact_model):
        self.result = ScenarioComparisonResult(
            scenarios_parameters=entry_data,
            impact_model=impact_model,
            by_property=self.by_property,
        )
        result_table = self.result.get_table()
        return result_table

    def fetch_from_lca_data(self, entry_data, lca_data):
        raise NotImplementedError()

    def run(
        self,
        entry_data,
        impact_model: ImpactModel = None,
        lca_data: pd.DataFrame = None,
    ):
        if entry_data["action"] == ACTION_ADD:
            self._state["scenario_parameters"][entry_data["scenario_name"]] = {
                **entry_data["parameters"]
            }
            scenario_scores = self.get_results(
                self._state["scenario_parameters"], impact_model, lca_data
            )
            fig = self.result.get_figure(scenario_scores)
            st.plotly_chart(fig)
        if entry_data["action"] == ACTION_CLEAR:
            self._state["scenario_parameters"] = {}


@register_panel("heatmap_dynamic_output_panel")
class HeatmapDynamicOutputPanel(DynamicOutputPanel):
    type: Literal["heatmap_dynamic_output_panel"]
    impact_method: str
    resolution: int = 64

    def compute_from_impact_model(self, entry_data, impact_model):
        self.result = HeatmapResult(
            impact_model=impact_model,
            x_parameter=entry_data["0"],
            y_parameter=entry_data["1"],
            impact_method=self.impact_method,
            resolution=self.resolution,
        )
        result_table = self.result.get_table()
        return result_table

    def fetch_from_lca_data(self, entry_data, lca_data):
        raise NotImplementedError()

    def run(
        self,
        entry_data,
        impact_model: ImpactModel = None,
        lca_data: pd.DataFrame = None,
    ):
        if entry_data["action"] == ACTION_ADD:
            scores = self.get_results(entry_data["parameters"], impact_model, lca_data)
            fig = self.result.get_figure(scores)
            st.plotly_chart(fig)
