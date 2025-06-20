# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 17:48:00 2022

@author: Ting-Hsu Chang
@email: Wanini.KLP.Mashimaro@gmail.com
"""

import os
import shutil

from ._common import ProjectInfo
from ._utils import write_text

_COPY_FILES = ['__init__.py',
               'build.py',
               'doc.py',
               'env.py',
               'git.py',
               'secure.py',
               'style.py',
               'test.py',
               'conda.py']


def _common(info: ProjectInfo) -> str:
    """Content-Generator for `_common.py` module."""
    ret = ("\"\"\"Common definitions\"\"\"\n\n"
           "import sys\n\n"
           "VENV_PREFIX = 'pipenv run'\n"
           f"_COMMON_TARGETS = ['{info.package}', 'tests', 'setup.py', 'tasks']\n"
           "COMMON_TARGETS_AS_STR = ' '.join(_COMMON_TARGETS)\n"
           f"TEST_TARGET = \"{info.package}\"\n\n"
           "# The differences between Linux and Windows\n"
           "USE_PTY = sys.platform != 'win32'\n")
    return ret


def gen_tasks(info: ProjectInfo):
    """Content-Generator for `tasks` package."""
    path = f'{info.path}/{info.name}/tasks'
    os.makedirs(path)
    for file in _COPY_FILES:
        shutil.copyfile(f'tasks/{file}', f'{path}/{file}')
    write_text(_common(info), f'{path}/_common.py')
