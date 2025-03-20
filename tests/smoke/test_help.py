"""
This test ensure that apparun --help works
"""

import subprocess


def test_help_command():
    result = subprocess.run(["apparun", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
