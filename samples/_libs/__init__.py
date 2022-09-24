# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 14:05:00 2022

@author: Ting-Hsu Chang
@email: Wanini.KLP.Mashimaro@gmail.com
"""

import os
from pathlib import Path

from ._common import ProjectInfo
from ._configs import gen_configs
from ._docs import gen_docs


def gen_project(info: ProjectInfo):
    path = f'{info.path}/{info.name}'
    os.makedirs(path)
    os.makedirs(f'{path}/{info.package}')
    Path(f'{path}/{info.package}/__init__.py').touch()
    os.makedirs(f'{path}/tests')
    gen_docs(info)
    gen_configs(info)
