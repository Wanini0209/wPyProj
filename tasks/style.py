"""Tasks for code-style.

Methods
-------
black:
    Reformat code through `black`.
black_check:
    Check code-style through `black`.
commit_check:
    Check commit message through `commitizen`.
flake8:
    Check code-style through `flake8`.
isort:
    Rearrange import-order through `isort`.
isort_check:
    Check import-order through `isort`.
mypy:
    Check static-type through `mypy`.
pylint:
    Check code-style through `pylint`.
reformat:
    Reformat code throguh `black` and `isort`.
run:
    Check code-style throguh linters.

"""
import sys

from invoke import task

from tasks._common import COMMON_TARGETS_AS_STR, VENV_PREFIX


@task
def flake8(ctx):
    """Check code-style through `flake8`"""
    ctx.run(f"{VENV_PREFIX} flake8 --config=setup.cfg")


@task
def mypy(ctx):
    """Check static-type through `mypy`"""
    ctx.run(f"{VENV_PREFIX} mypy")


@task
def black_check(ctx):
    """Check code-style through `black`"""
    ctx.run(f"{VENV_PREFIX} black --check {COMMON_TARGETS_AS_STR}")


@task
def isort_check(ctx):
    """Check import-order through `isort`"""
    ctx.run(f"{VENV_PREFIX} isort {COMMON_TARGETS_AS_STR} --atomic --check-only")


@task
def commit_check(ctx):
    """Check commit message through `commitizen`"""
    result = ctx.run(f"{VENV_PREFIX} cz check --rev-range master..", warn=True)
    if result.exited == 3:  # NO_COMMIT_FOUND
        sys.exit(0)
    else:
        sys.exit(result.exited)


@task
def pylint(ctx):
    """Check code-style through `pylint`"""
    ctx.run(f"{VENV_PREFIX} pylint {COMMON_TARGETS_AS_STR}")


@task
def black(ctx):
    """Reformat code through `black`"""
    ctx.run(f"{VENV_PREFIX} black {COMMON_TARGETS_AS_STR}")


@task
def isort(ctx):
    """Rearrange import-order through `isort`"""
    ctx.run(f"{VENV_PREFIX} isort {COMMON_TARGETS_AS_STR} --atomic --apply")


# pylint: disable=unused-argument
# `ctx` is required for `invoke` task
@task(pre=[flake8, mypy, isort_check], default=True)
def run(ctx):
    """Check code-style throguh linters.

    Check code-style through `flake`;
    Check static-type through `mypy`;
    Check import-order through `isort`.

    Notes
    -----
    `pylint` is not included and
    only to check code-style not to reformat.

    """


@task(pre=[black, isort])
def reformat(ctx):
    """Reformat code throguh `black` and `isort`"""
