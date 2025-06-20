"""Tasks for testing.

Methods
-------
cov:
    Check test coverage through `pytest-cov`.
run:
    Run test cases through `pytest`.

"""
from invoke import task

from tasks._common import TEST_TARGET, USE_PTY, VENV_PREFIX

PYTEST = f"{VENV_PREFIX} pytest"


@task(default=True)
def run(ctx):
    """Run test cases"""
    ctx.run(PYTEST, pty=USE_PTY)


@task
def cov(ctx):
    """Check test covreage"""
    ctx.run(f"{PYTEST} --cov={TEST_TARGET} --cov-report=html", pty=USE_PTY)
