"""Task file generators."""

import os
import shutil

from ._common import ProjectInfo
from ._utils import write_text

_COPY_FILES = [
    "__init__.py",
    "build.py",
    "doc.py",
    "env.py",
    "git.py",
    "secure.py",
    "style.py",
    "test.py",
    "conda.py",
]


def _common(info: ProjectInfo) -> str:
    """Content-Generator for `_common.py` module."""
    ret = (
        '"""Common definitions for invoke tasks.\\n\\n'
        "This module contains common constants and configurations used across\\n"
        "all task modules.\\n\\n"
        "Attributes\\n"
        "----------\\n"
        "VENV_PREFIX : str\\n"
        "    Prefix command for running commands in virtual environment.\\n"
        "COMMON_TARGETS : list of str\\n"
        "    List of common target directories for various tasks.\\n"
        "COMMON_TARGETS_AS_STR : str\\n"
        "    Space-separated string of common targets.\\n"
        "TEST_TARGET : str\\n"
        "    Default target directory for testing.\\n"
        "USE_PTY : bool\\n"
        "    Whether to use pseudo-terminal based on platform.\\n\\n"
        '"""\\n\\n'
        "import sys\\n\\n"
        'VENV_PREFIX: str = "pipenv run"\\n'
        f'COMMON_TARGETS: list[str] = ["{info.package}", "tests", "setup.py", "tasks"]\\n'  # noqa: E501
        'COMMON_TARGETS_AS_STR: str = " ".join(COMMON_TARGETS)\\n'
        f'TEST_TARGET: str = "{info.package}"\\n\\n'
        "# The differences between Linux and Windows\\n"
        'USE_PTY: bool = sys.platform != "win32"\\n'
    )
    return ret


def gen_tasks(info: ProjectInfo):
    """Content-Generator for `tasks` package."""
    path = f"{info.path}/{info.name}/tasks"
    os.makedirs(path)
    for file in _COPY_FILES:
        shutil.copyfile(f"tasks/{file}", f"{path}/{file}")
    write_text(_common(info), f"{path}/_common.py")
