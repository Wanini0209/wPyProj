# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 14:09:00 2022

@author: Ting-Hsu Chang
@email: Wanini.KLP.Mashimaro@gmail.com
"""

from typing import NamedTuple


class ProjectInfo(NamedTuple):
    """Project Information."""
    path: str
    url: str
    name: str
    description: str
    package: str
    author: str
    email: str
    version: str
