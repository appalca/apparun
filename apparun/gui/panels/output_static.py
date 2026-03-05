from typing import Literal

import pandas as pd
import streamlit as st

from apparun.gui.panels.base import StaticOutputPanel, register_panel
from apparun.impact_model import ImpactModel
from apparun.results import ImpactModelResult


@register_panel("markdown")
class Markdown(StaticOutputPanel):
    type: Literal["markdown"]
    message: str

    def run(self, impact_model: ImpactModel = None, lca_data: pd.DataFrame = None):
        st.markdown(f"{self.message}")
