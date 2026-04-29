"""
This module contains the tests related to the gui command.
"""

from streamlit.testing.v1 import AppTest


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
