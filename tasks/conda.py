"""Tasks for Conda Develope Environments.

Methods
-------
pip_freeze:
    Generate requirements via `pip freeze`.
update:
    Update local Conda information.
create:
    Create Conda develop environment.
remove:
    Remove Conda develop environment.
activate:
    Activate Conda develop environment.

"""
import datetime
import json
import os
import subprocess
from typing import Dict, NamedTuple, Optional, Union

from invoke import task

from tasks._common import VENV_PREFIX

_REQURIEMENTS_FILE = '.pip_freeze'
_CONDA_INFO_FILE = '.conda'
_PROJ_INFO_FILE = '.info'
_MAX_64BYTE_INT = 0xFFFFFFFFFFFFFFFF


def get_cmd_out(cmd: str, encoding: str = 'utf-8'):
    recv = subprocess.check_output(cmd, shell=True)
    ret = recv.decode(encoding)
    return ret.strip()


def get_random_env_name(prefix: str) -> str:
    now = datetime.datetime.now()
    suffix = hex(hash(now) & _MAX_64BYTE_INT)
    assert suffix[:2] == '0x'
    ret = f'{prefix}_{suffix[2:]}'
    return ret


class CondaInfo(NamedTuple):
    """Conda Environment Information."""
    python_version: str
    env_name: str
    conda_path: Optional[str] = None
    conda_cmd: Optional[str] = None
    activate_cmd: Optional[str] = None

    def to_dict(self) -> Dict[str, str]:
        ret = {'condaCmd': self.conda_cmd,
               'activateCmd': self.activate_cmd,
               'envName': self.env_name,
               'condaRoot': self.conda_path,
               'pyVer': self.python_version}
        return ret

    def dump2json(self, file: str):
        with open(file, 'w', encoding='utf-8') as fout:
            json.dump(self.to_dict(), fout)

    @classmethod
    def from_dict(cls, recv: Dict[str, str]) -> 'CondaInfo':
        conda_cmd = recv['condaCmd']
        if not os.path.exists(conda_cmd):
            conda_cmd = None

        activate_cmd = recv['activateCmd']
        if not os.path.exists(activate_cmd):
            activate_cmd = None

        conda_path = recv['condaRoot']
        if not os.path.exists(conda_path):
            conda_path = None

        env_name = recv['envName']
        python_version = recv['pyVer']
        ret = cls(python_version=python_version,
                  env_name=env_name,
                  conda_path=conda_path,
                  conda_cmd=conda_cmd,
                  activate_cmd=activate_cmd)
        return ret

    @classmethod
    def load4json(cls, file: str) -> 'CondaInfo':
        with open(file, 'r', encoding='utf-8') as fin:
            recv = json.load(fin)
        return cls.from_dict(recv)

    @classmethod
    def make(cls, project_name: str, python_version: str) -> 'CondaInfo':
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


def _get_conda_info() -> Union[None, CondaInfo]:
    if os.path.exists(_CONDA_INFO_FILE):
        ret = CondaInfo.load4json(_CONDA_INFO_FILE)
        return ret
    return None


def _update_conda_info(info: CondaInfo):
    info.dump2json(_CONDA_INFO_FILE)


def get_proj_info() -> Dict[str, str]:
    with open(_PROJ_INFO_FILE, 'r', encoding='utf-8') as f:
        ret = json.load(f)
    return ret


@task
def freeze(ctx):
    """Generate requirements file via `pip freeze`"""
    ctx.run(f"{VENV_PREFIX} pip freeze > {_REQURIEMENTS_FILE}")


@task
def update(ctx):
    """Update local Conda information"""
    proj_info = get_proj_info()
    info = CondaInfo.make(proj_info['name'], proj_info['version'])
    _update_conda_info(info)


@task(pre=[update])
def create(ctx):
    """Create Conda develop environment"""
    info = _get_conda_info()
    if info is None:
        raise RuntimeError("Please run `update` before `create`")
    os.system(f"{info.conda_cmd} "
              f"create --name {info.env_name} "
              f"python={info.python_version}")


@task
def remove(ctx):
    """Remove Conda develop environment"""
    info = _get_conda_info()
    if info is None:
        raise RuntimeError("Please run `create` before `remove`")
    os.system(f"{info.conda_cmd} "
              f"remove --name {info.env_name} --all")


@task
def activate(ctx):
    """Activate Conda develop environment"""
    info = _get_conda_info()
    if info is None:
        raise RuntimeError("Please run `create` before `activate`")
    os.system("start cmd /s /k "
              f"{info.activate_cmd} "
              f"{info.env_name}")
