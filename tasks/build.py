"""Task for build.

Methods
-------
clean:
    Remove all the tmp files in `.gitignore`.
develop:
    Install environment in development mode.
dist:
    Build distribution.
install:
    Install environment in product mode.
requirements:
    Generate requirements via `Pipfile`.

"""

import json
import os
import tomllib

from invoke import Collection, Context, task

from tasks import style, test
from tasks._common import VENV_PREFIX

REQUIREMENTS_FILE: str = "requirements.txt"
REQUIREMENTS_DEV_FILE: str = "requirements-dev.txt"
PIPFILE: str = "Pipfile"
PIPFILE_LOCK: str = "Pipfile.lock"


def load_pipfile_lock() -> dict:
    """Load Pipfile.lock content.

    Returns
    -------
    dict
        The content of Pipfile.lock, empty dict if file not exists.

    """
    if not os.path.exists(PIPFILE_LOCK):
        return {}

    with open(PIPFILE_LOCK, encoding="utf-8") as fin:
        ret = json.load(fin)
    return ret


def pipfile_to_requirements() -> dict[str, dict[str, str]]:
    """Convert Pipfile to requirements format.

    Returns
    -------
    dict
        Dictionary with 'common' and 'develop' keys containing
        package names and versions.

    Notes
    -----
    This function parses both Pipfile and Pipfile.lock to extract
    package information with pinned versions.

    """
    if not os.path.exists(PIPFILE):
        return {"common": {}, "develop": {}}

    locks = load_pipfile_lock()
    ret: dict[str, dict[str, str]] = {"common": {}, "develop": {}}

    # 使用 tomllib 讀取 Pipfile
    with open(PIPFILE, "rb") as fin:
        pipfile_data = tomllib.load(fin)

    # 處理 packages (common)
    for pkg in pipfile_data.get("packages", {}):
        if pkg in locks.get("default", {}):
            ret["common"][pkg] = locks["default"][pkg]["version"]

    # 處理 dev-packages (develop)
    for pkg in pipfile_data.get("dev-packages", {}):
        if pkg in locks.get("develop", {}):
            ret["develop"][pkg] = locks["develop"][pkg]["version"]

    return ret


@task
def requirements(ctx: Context) -> None:
    """Generate requirements file from `Pipfile`.

    Parameters
    ----------
    ctx : invoke.Context
        The invoke context object.

    Notes
    -----
    This task generates two files:
    - requirements.txt: production dependencies only
    - requirements-dev.txt: both production and development dependencies

    """
    reqs = pipfile_to_requirements()

    with open(REQUIREMENTS_FILE, "w", encoding="utf-8") as fout:
        fout.writelines([f"{pkg}{ver}\n" for pkg, ver in reqs["common"].items()])

    with open(REQUIREMENTS_DEV_FILE, "w", encoding="utf-8") as fout:
        fout.writelines([f"{pkg}{ver}\n" for pkg, ver in reqs["common"].items()])
        fout.writelines([f"{pkg}{ver}\n" for pkg, ver in reqs["develop"].items()])


@task
def develop(ctx: Context) -> None:
    """Install script in pipenv environment in development mode.

    Parameters
    ----------
    ctx : invoke.Context
        The invoke context object.

    Notes
    -----
    This installs the package in editable/development mode, allowing
    changes to the source code to be immediately reflected without
    reinstallation.

    """
    ctx.run(f"{VENV_PREFIX} python setup.py develop")


@task
def install(ctx: Context) -> None:
    """Install script in pipenv environment.

    Parameters
    ----------
    ctx : invoke.Context
        The invoke context object.

    Notes
    -----
    This installs the package in production mode.

    """
    ctx.run(f"{VENV_PREFIX} python setup.py install")


@task(pre=[style.run, test.run])
def dist(ctx: Context) -> None:
    """Build distribution.

    Parameters
    ----------
    ctx : invoke.Context
        The invoke context object.

    Notes
    -----
    This task runs style checks and tests before building
    source and wheel distributions.

    """
    ctx.run(f"{VENV_PREFIX} python setup.py sdist bdist_wheel")


@task
def clean(ctx: Context) -> None:
    """Remove all the tmp files in `.gitignore`.

    Parameters
    ----------
    ctx : invoke.Context
        The invoke context object.

    Notes
    -----
    This uses git clean to remove all ignored files. Use with caution
    as this will delete all untracked files matching .gitignore patterns.

    """
    ctx.run("git clean -Xdf")


build_ns = Collection("build")
build_ns.add_task(requirements)
build_ns.add_task(develop)
build_ns.add_task(install)
build_ns.add_task(dist)
build_ns.add_task(clean)
