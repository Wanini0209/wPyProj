"""Common definitions for invoke tasks.

This module contains common constants and configurations used across
all task modules.

Attributes
----------
VENV_PREFIX : str
    Prefix command for running commands in virtual environment.
COMMON_TARGETS : list of str
    List of common target directories for various tasks.
COMMON_TARGETS_AS_STR : str
    Space-separated string of common targets.
TEST_TARGET : str
    Default target directory for testing.
USE_PTY : bool
    Whether to use pseudo-terminal based on platform.

"""

import sys

VENV_PREFIX: str = "pipenv run"
COMMON_TARGETS: list[str] = ["samples", "tests", "setup.py", "tasks"]
COMMON_TARGETS_AS_STR: str = " ".join(COMMON_TARGETS)
# [FIX] 將 wsatools 修正為 samples
TEST_TARGET: str = "samples"

# The differences between Linux and Windows
USE_PTY: bool = sys.platform != "win32"
