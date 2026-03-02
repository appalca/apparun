from __future__ import annotations

import subprocess
from typing import Annotated, Any, Callable, Dict, List, Optional, TypeVar, Union

import pandas as pd
import streamlit as st
from pydantic import BaseModel, Field, field_validator

from apparun.gui.panels.base import *
from apparun.gui.panels.base import (
    InputPanel,
    OutputPanel,
    get_input_panel,
    get_output_panel,
)
from apparun.gui.panels.output_dynamic import *
from apparun.gui.panels.output_static import *
from apparun.impact_model import ImpactModel

PandasDataFrame = TypeVar("pd.core.frame.DataFrame")


class Module(BaseModel):
    name: Optional[str] = None
    lca_data_path: Optional[str] = None
    impact_model_path: Optional[str] = None
    input_panel: Optional[InputPanel] = None
    output_panels: List[OutputPanel]
    cols: Optional[Callable] = None
    lca_data: Optional[PandasDataFrame] = None
    impact_model: Optional[ImpactModel] = None

    @field_validator("input_panel", mode="before")
    @classmethod
    def build_input_panel(
        cls, panel: Optional[Dict[Any]] = None
    ) -> Optional[InputPanel]:
        if panel is None:
            return None
        return get_input_panel(panel["type"])(**panel)

    @field_validator("output_panels", mode="before")
    @classmethod
    def build_output_panels(cls, panels: List[Dict[Any]]) -> List[OutputPanel]:
        return [
            get_output_panel(output_panel["type"])(**output_panel)
            for output_panel in panels
        ]

    def __init__(self, **args):
        super().__init__(**args)
        self.lca_data = (
            pd.read_csv(self.lca_data_path) if self.lca_data_path is not None else None
        )
        self.impact_model = (
            ImpactModel.from_yaml(self.impact_model_path)
            if self.impact_model_path is not None
            else None
        )

    @property
    def input_col(self):
        if self.cols is None:
            return None
        if self.input_panel is None:
            return None
        return self.cols[0]

    @property
    def output_col(self):
        if self.cols is None:
            return None
        if self.input_panel is None:
            return self.cols[0]
        return self.cols[1]

    @st.fragment()
    def run(self):
        self.cols = (
            st.columns(1) if self.input_panel is None else st.columns([0.33, 0.67])
        )
        if self.input_panel is not None:
            with self.input_col:
                self.input_panel.run()
            with self.output_col:
                for output_panel in self.output_panels:
                    output_panel.run(
                        self.input_panel.state,
                        impact_model=self.impact_model,
                        lca_data=self.lca_data,
                    )
        else:
            with self.output_col:
                for output_panel in self.output_panels:
                    output_panel.run(
                        impact_model=self.impact_model, lca_data=self.lca_data
                    )


class GUI(BaseModel):
    name: Optional[str] = None
    modules: List[Module]

    def setup_layout(self):
        st.html(
            """
            <style>
                .stMainBlockContainer {
                    max-width:70rem;
                }
            </style>
            """
        )

    def gen_titles_modules(self):
        if self.name is not None:
            self.modules.insert(
                0,
                Module(
                    **{
                        "output_panels": [
                            {"type": "markdown", "message": f"# {self.name}"}
                        ]
                    }
                ),
            )
        modules_with_titles = []
        for module in self.modules:
            if module.name is None:
                modules_with_titles.append(module)
            else:
                modules_with_titles.append(
                    Module(
                        **{
                            "output_panels": [
                                {"type": "markdown", "message": f"## {module.name}"}
                            ]
                        }
                    )
                )
                modules_with_titles.append(module)
        self.modules = modules_with_titles

    def run(self):
        self.gen_titles_modules()
        containers = [st.container() for i in range(len(self.modules))]
        for i in range(len(self.modules)):
            with containers[i]:
                self.modules[i].run()
