"""Tasks for `git`.

Methods
-------
commit:
    Commit through `commitizen`.
bump:
    Bump version through `commitizen`.

"""
import sys

from invoke import task

from tasks._common import USE_PTY, VENV_PREFIX


@task
def commit(ctx):
    """Commit through `commitizen`"""
    ctx.run(f"{VENV_PREFIX} cz commit", pty=USE_PTY)


@task
def bump(ctx, with_changelog=False):
    """Bump version through `commitizen`"""
    argument = ""
    if with_changelog:
        argument += " --changelog"

    result = ctx.run(f"{VENV_PREFIX} cz bump --yes{argument}", warn=True)
    if result.exited == 3:  # NO_COMMIT_FOUND
        sys.exit(0)
    else:
        sys.exit(result.exited)
