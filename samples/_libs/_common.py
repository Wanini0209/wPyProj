# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 14:09:00 2022

@author: Ting-Hsu Chang
@email: Wanini.KLP.Mashimaro@gmail.com
"""

import json
from typing import Dict, NamedTuple


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

    def to_dict(self) -> Dict[str, str]:
        ret = {'path': self.path,
               'url': self.url,
               'name': self.name,
               'description': self.description,
               'package': self.package,
               'author': self.author,
               'email': self.email,
               'version': self.version}
        return ret

    def dump2json(self, file: str):
        with open(file, 'w', encoding='utf-8') as fout:
            json.dump(self.to_dict(), fout)

    @classmethod
    def from_dict(cls, recv: Dict[str, str]) -> 'ProjectInfo':
        return cls(**recv)

    @classmethod
    def load4json(cls, file: str) -> 'ProjectInfo':
        with open(file, 'r', encoding='utf-8') as fin:
            recv = json.load(fin)
        return cls.from_dict(recv)
