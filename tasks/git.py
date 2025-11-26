"""Tasks for `git`.

Methods
-------
commit:
    Commit through `commitizen`.
bump:
    Bump version through `commitizen`.

"""

import sys

from invoke import Context, task

from tasks._common import USE_PTY, VENV_PREFIX

NO_COMMIT_FOUND: int = 3


@task
def commit(ctx: Context) -> None:
    """Commit through `commitizen`.

    Parameters
    ----------
    ctx : invoke.Context
        The invoke context object.

    Notes
    -----
    This uses commitizen to create standardized commit messages
    following conventional commits specification.

    """
    ctx.run(f"{VENV_PREFIX} cz commit", pty=USE_PTY)


@task
def bump(ctx: Context, with_changelog: bool = False) -> None:
    """Bump version through `commitizen`.

    Parameters
    ----------
    ctx : invoke.Context
        The invoke context object.
    with_changelog : bool, optional
        Generate changelog when bumping version, by default False.

    Notes
    -----
    This automatically determines the next version based on commit
    messages and updates version numbers throughout the project.
    Exit code 3 (NO_COMMIT_FOUND) is treated as success.

    """
    argument = ""
    if with_changelog:
        argument += " --changelog"

    result = ctx.run(f"{VENV_PREFIX} cz bump --yes{argument}", warn=True)

    # 使用常數代替數字 3
    if result.exited == NO_COMMIT_FOUND:
        sys.exit(0)
    else:
        sys.exit(result.exited)
