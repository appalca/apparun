"""
This module contains the tests related to the gui command.
"""

from streamlit.testing.v1 import AppTest


def run_test_gui():
    from apparun.cli.main import generate_gui

    generate_gui("tests/data/conf/functional_gui.yaml")


def test_streamlit_app_is_deploying():
    """
    Check that the streamlit app initialized by sample conf is deploying.
    """

    at = AppTest.from_function(run_test_gui, default_timeout=10)
    at.run()
    # This app should generate three md widgets: one title, one header, one text block.
    assert len(at.markdown) == 3
