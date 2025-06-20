"""Tasks for code-security.

Methods
-------
check_package:
    Check package security through `pipenv`.
bandit:
    Check common software vulnerabilities through `bandit`.

"""
from invoke import task

from tasks._common import USE_PTY, VENV_PREFIX


@task(default=True)
def check_package(ctx):
    """Check package security through `pipenv`"""
    ctx.run("pipenv check")


@task
def bandit(ctx):
    """Check common software vulnerabilities through `bandit`.

    Notes
    -----
    It is only used as reference.

    """
    ctx.run(f"{VENV_PREFIX} bandit -r -iii -lll --ini .bandit", pty=USE_PTY)
