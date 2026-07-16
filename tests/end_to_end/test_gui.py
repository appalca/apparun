"""
This module contains the tests related to the gui command.
"""

import pytest
from PIL import UnidentifiedImageError
from streamlit.testing.v1 import AppTest

from apparun.cli.main import load_yaml
from apparun.gui.modules import GUI


def run_test_gui():
    import streamlit as st

    from apparun.cli.main import gui

    st.query_params["gui_config_path"] = "samples/conf/sample_gui.yaml"
    gui()


def test_streamlit_app_is_deploying():
    """
    Check that the streamlit app initialized by sample conf is deploying.
    """

    at = AppTest.from_function(run_test_gui, default_timeout=10)
    at.run()
    # This app should generate seven md widgets: one page title, five header, one text block.
    assert len(at.markdown) == 7


def test_favicons():
    """
    Check that local and remote favicon can be loaded.
    """
    remote_logo_gui_config = load_yaml("tests/data/conf/functional_gui.yaml", "r")
    gui = GUI(**remote_logo_gui_config)
    try:
        gui.setup_layout()
    except UnidentifiedImageError:
        msg = f"Cannot load remote favicon {gui.favicon_path}"
        pytest.fail(msg)

    local_logo_gui_config = load_yaml(
        "tests/data/conf/functional_gui_local_logo.yaml", "r"
    )
    gui = GUI(**local_logo_gui_config)
    try:
        gui.setup_layout()
    except UnidentifiedImageError:
        msg = f"Cannot load local favicon {gui.favicon_path}"
        pytest.fail(msg)
