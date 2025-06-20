"""Tasks for Conda Develope Environments.

Methods
-------
pip_freeze:
    Generate requirements via `pip freeze`.
create:
    Create Conda develop environment.
activate:
    Activate Conda develop environment.

"""

import json
import os
import sys
import subprocess
from invoke import task

from tasks._common import VENV_PREFIX

_REQURIEMENTS_FILE = '.pip_freeze'

_CONDA_INFO = json.load(open('.conda', 'r', encoding='utf-8'))

@task
def freeze(ctx):
    """Generate requirements file via `pip freeze`"""
    ctx.run(f"{VENV_PREFIX} pip freeze > {_REQURIEMENTS_FILE}")


@task
def create(ctx):
    """Create Conda develop environment"""
    os.system(f"{_CONDA_INFO['condaCmd']} "
              f"create --name {_CONDA_INFO['envName']} "
              f"python={_CONDA_INFO['pythonVersion']}")

@task
def remove(ctx):
    """Remove Conda develop environment"""
    os.system(f"{_CONDA_INFO['condaCmd']} "
              f"remove --name {_CONDA_INFO['envName']} --all")

@task
def activate(ctx):
    """Activate Conda develop environment"""
    os.system("start cmd /s /k "
              f"{_CONDA_INFO['activateCmd']} "
              f"{_CONDA_INFO['envName']}")
