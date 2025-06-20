# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 14:05:00 2022

@author: Ting-Hsu Chang
@email: Wanini.KLP.Mashimaro@gmail.com
"""

import os
from pathlib import Path
import shutil

from ._common import CondaInfo, ProjectInfo
from ._configs import gen_configs
from ._docs import gen_docs
from ._tasks import gen_tasks


def gen_project(info: ProjectInfo):
    """Project Generator."""
    path = f'{info.path}/{info.name}'
    os.makedirs(path)
    os.makedirs(f'{path}/{info.package}')
    Path(f'{path}/{info.package}/__init__.py').touch()
    os.makedirs(f'{path}/tests')
    shutil.copyfile(f'tests/test_placeholder.py', f'{path}/tests/test_placeholder.py')
    gen_docs(info)
    gen_configs(info)
    gen_tasks(info)
    if info.conda_info is not None:
        info.conda_info.dump2json(f'{path}/.conda')
