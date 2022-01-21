"""Common definitions"""

import sys

VENV_PREFIX = "pipenv run"
_COMMON_TARGETS = ["samples", "tests", "setup.py", "tasks"]
COMMON_TARGETS_AS_STR = " ".join(_COMMON_TARGETS)

# The differences between Linux and Windows
USE_PTY = sys.platform != 'win32'
