"""Task for build.

Methods
-------
clean:
    Remove all the tmp files in `.gitignore`.
develop:
    Install environement in development mode.
dist:
    Build distribution.
install:
    Install environement in product mode.
requirements:
    Generate requirements via `Pipfile`.

"""
import json
import os
import re
from typing import Dict

from invoke import Collection, task

from tasks import style, test
from tasks._common import VENV_PREFIX


_REQURIEMENTS_FILE = 'requirements.txt'
_REQURIEMENTS_DEV_FILE = 'requirements-dev.txt'
_PIPFILE = 'Pipfile'
_PIPFILE_LOCK = 'Pipfile.lock'


def load_pipfile_lock() -> dict:
    if not os.path.exists(_PIPFILE_LOCK):
        return {}
    with open(_PIPFILE_LOCK, 'r') as fin:
        ret = json.load(fin)
    return ret


def pipfile2requirements() -> Dict[str, str]:
    if not os.path.exists(_PIPFILE):
        return {}
    locks = load_pipfile_lock()
    ret = {'common': {}, 'develop': {}}
    with open(_PIPFILE, 'r') as fin:
        title: str = ''
        for line in fin.readlines():
            try:
                title = re.findall(r'^\[(.*?)\]$', line)[0]
            except IndexError:
                if len(line) > 1:
                    if title == 'packages':
                        pkg = re.findall(r'^([^=]+)=', line)[0].strip()
                        ret['common'][pkg] = locks['default'][pkg]['version']
                    if title == 'dev-packages':
                        pkg = re.findall(r'^([^=]+)=', line)[0].strip()
                        ret['develop'][pkg] = locks['develop'][pkg]['version']
    return ret


@task
def requirements(ctx):
    """Generate requirements file from `Pipfile`"""
    requirements = pipfile2requirements()
    with open(_REQURIEMENTS_FILE, 'w') as fout:
        fout.writelines([f'{pkg}{ver}\n'
            for pkg, ver in requirements['common'].items()])
    with open(_REQURIEMENTS_DEV_FILE, 'w') as fout:
        fout.writelines([f'{pkg}{ver}\n'
            for pkg, ver in requirements['common'].items()])
        fout.writelines([f'{pkg}{ver}\n'
            for pkg, ver in requirements['develop'].items()])


@task
def develop(ctx):
    """Install script in pipenv environement in development mode"""
    ctx.run(f"{VENV_PREFIX} python setup.py develop")


@task
def install(ctx):
    """Install script in pipenv environement"""
    ctx.run(f"{VENV_PREFIX} python setup.py install")


@task(pre=[style.run, test.run])
def dist(ctx):
    """Build distribution"""
    ctx.run(f"{VENV_PREFIX} python setup.py sdist bdist_wheel")


@task
def clean(ctx):
    """Remove all the tmp files in `.gitignore`"""
    ctx.run("git clean -Xdf")


build_ns = Collection("build")
build_ns.add_task(requirements)
build_ns.add_task(develop)
build_ns.add_task(install)
build_ns.add_task(dist)
build_ns.add_task(clean)
