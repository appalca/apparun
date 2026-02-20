from typing import Literal

import streamlit as st

from apparun.gui.panels.base import StaticOutputPanel, register_panel
from apparun.results import ImpactModelResult


@register_panel("markdown")
class Markdown(StaticOutputPanel):
    type: Literal["markdown"]
    message: str

    def run(self):
        st.markdown(f"{self.message}")
