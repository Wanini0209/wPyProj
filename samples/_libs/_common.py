# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 14:09:00 2022

@author: Ting-Hsu Chang
@email: Wanini.KLP.Mashimaro@gmail.com
"""

import datetime
import json
import os
import subprocess

from typing import Dict, NamedTuple, Optional

def get_cmd_out(cmd: str, encoding: str='utf-8'):
    recv = subprocess.check_output(cmd, shell=True)
    ret = recv.decode(encoding)
    return ret.strip()


_MAX_64BYTE_INT = 0xFFFFFFFFFFFFFFFF
def get_random_env_name(prefix: str) -> str:
    now = datetime.datetime.now()
    suffix = hex(hash(now) & _MAX_64BYTE_INT)
    assert suffix[:2] == '0x'
    ret = f'{prefix}_{suffix[2:]}'
    return ret


class CondaInfo(NamedTuple):
    """Conda Environment Information."""
    conda_path: str
    conda_cmd: str
    activate_cmd: str
    env_name: str
    python_version: str

    def to_dict(self) -> Dict[str, str]:
        ret = {'condaCmd': self.conda_cmd,
               'activateCmd': self.activate_cmd,
               'envName': self.env_name,
               'condaRoot': self.conda_path,
               'pythonVersion': self.python_version}
        return ret

    def dump2json(self, file: str):
        with open(file, 'w', encoding='utf-8') as fout:
            json.dump(self.to_dict(), fout)

    @classmethod
    def make(cls, project_name: str, python_version: str):
        conda_cmd = get_cmd_out("where conda")
        assert conda_cmd[-10:] == '\\conda.bat'
        condabin_path = conda_cmd[:-10]
        assert os.path.exists(condabin_path)
        activate_cmd = f'{condabin_path}\\activate.bat'
        assert os.path.exists(activate_cmd)
        conda_path = '\\'.join(condabin_path.split('\\')[:-1])
        assert os.path.exists(conda_path)
        env_name = get_random_env_name(project_name)
        ret = cls(conda_path=conda_path,
                  conda_cmd=conda_cmd,
                  activate_cmd=activate_cmd,
                  env_name=env_name,
                  python_version=python_version)
        return ret


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
    conda_info: Optional[CondaInfo]=None
