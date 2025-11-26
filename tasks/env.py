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

from invoke import Context, task

from tasks._common import VENV_PREFIX


@task
def clean(ctx: Context) -> None:
    """Remove virtual environment.

    Parameters
    ----------
    ctx : invoke.Context
        The invoke context object.

    Notes
    -----
    This will completely remove the pipenv virtual environment.
    Use with caution as all installed packages will be lost.

    """
    ctx.run("pipenv --rm", warn=True)


@task
def init(ctx: Context) -> None:
    """Install production dependencies.

    Parameters
    ----------
    ctx : invoke.Context
        The invoke context object.

    Notes
    -----
    This installs only the production dependencies specified in
    Pipfile, using the exact versions from Pipfile.lock.

    """
    ctx.run("pipenv install --deploy")


@task
def setup_pre_commit_hook(ctx: Context) -> None:
    """Set up pre-commit hook.

    Parameters
    ----------
    ctx : invoke.Context
        The invoke context object.

    Notes
    -----
    This sets up pre-commit hooks for:
    - pre-commit: runs before each commit
    - pre-push: runs before each push
    - commit-msg: validates commit messages

    """
    ctx.run("git init")
    ctx.run(
        f"{VENV_PREFIX} pre-commit install -t pre-commit & "
        f"{VENV_PREFIX} pre-commit install -t pre-push & "
        f"{VENV_PREFIX} pre-commit install -t commit-msg"
    )


@task(optional=["without-pre-commit"])
def init_dev(ctx: Context, without_pre_commit: bool = False) -> None:
    """Install development dependencies and set up pre-commit hooks.

    Parameters
    ----------
    ctx : invoke.Context
        The invoke context object.
    without_pre_commit : bool, optional
        Skip pre-commit hook setup if True, by default False.

    Notes
    -----
    This installs both production and development dependencies.
    Pre-commit hooks are configured automatically unless disabled.

    """
    ctx.run("pipenv install --dev")
    if not without_pre_commit:
        setup_pre_commit_hook(ctx)
