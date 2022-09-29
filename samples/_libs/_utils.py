# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 12:13:00 2022

@author: Ting-Hsu Chang
@email: Wanini.KLP.Mashimaro@gmail.com
"""


def read_text(file: str, encoding: str = 'utf-8') -> str:
    """Read content from text file."""
    with open(file, 'r', encoding=encoding) as src:
        ret = src.read()
    return ret


def write_text(data: str, file: str, encoding: str = 'utf-8'):
    """Read content from text file."""
    with open(file, 'w', encoding=encoding) as dst:
        dst.write(data)
