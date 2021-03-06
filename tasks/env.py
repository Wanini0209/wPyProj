"""Task for environment.

Methods
-------
clean:
    Remove virtual environment.
init:
    Establish product environment.
init_dev:
    Establish development environment.
setup_pre_commit_hook:
    Setup pre-commit hook.

"""
from invoke import task

from tasks._common import VENV_PREFIX


@task
def clean(ctx):
    """Remove virtual environement"""
    ctx.run("pipenv --rm", warn=True)


@task
def init(ctx):
    """Install production dependencies"""
    ctx.run("pipenv install --deploy")


@task
def setup_pre_commit_hook(ctx):
    """Setup pre-commit hook"""
    ctx.run("git init")
    ctx.run(
        f"{VENV_PREFIX} pre-commit install -t pre-commit & "
        f"{VENV_PREFIX} pre-commit install -t pre-push & "
        f"{VENV_PREFIX} pre-commit install -t commit-msg"
    )


@task(optional=["without-pre-commit"])
def init_dev(ctx, without_pre_commit=False):
    """Install development dependencies and setup pre-commit hooks"""
    ctx.run("pipenv install --dev")
    if not without_pre_commit:
        setup_pre_commit_hook(ctx)
