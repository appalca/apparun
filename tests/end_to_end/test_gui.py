"""
This module contains the tests related to the gui command.
"""

import pytest
from PIL import UnidentifiedImageError
from streamlit.testing.v1 import AppTest

from apparun.cli.main import load_yaml
from apparun.gui.modules import GUI


def run_test_gui():
    from apparun.cli.main import generate_gui

    generate_gui("tests/data/conf/functional_gui.yaml")


def run_multi_tab_test_gui():
    from apparun.cli.main import generate_gui

    generate_gui("tests/data/conf/functional_multi_tab_gui.yaml")


def test_streamlit_app_is_deploying():
    """
    Check that the streamlit app initialized by sample conf is deploying.
    """

    at = AppTest.from_function(run_test_gui, default_timeout=10)
    at.run()
    # This app should generate three md widgets: one title, one header, one text block.
    assert len(at.markdown) == 3


def test_multi_tab_streamlit_app_is_deploying():
    """
    Check that the streamlit app initialized by sample conf is deploying.
    """

    at = AppTest.from_function(run_multi_tab_test_gui, default_timeout=10)
    at.run()
    # five md widgets: one title, plus one header and one text block per tab.
    assert len(at.tabs) == 2
    assert len(at.tabs[0]) == 2
    assert len(at.tabs[1]) == 2
    assert len(at.markdown) == 5


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
