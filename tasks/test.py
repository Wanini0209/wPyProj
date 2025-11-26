"""Tasks for testing.

Methods
-------
cov:
    Check test coverage through `pytest-cov`.
run:
    Run test cases through `pytest`.

"""

from invoke import Context, task

from tasks._common import TEST_TARGET, USE_PTY, VENV_PREFIX

PYTEST: str = f"{VENV_PREFIX} pytest"


@task(default=True)
def run(ctx: Context) -> None:
    """Run test cases.

    Parameters
    ----------
    ctx : invoke.Context
        The invoke context object.

    Notes
    -----
    This runs all test cases using pytest. The USE_PTY flag is set
    based on the platform to ensure proper terminal interaction.

    """
    ctx.run(PYTEST, pty=USE_PTY)


@task
def cov(ctx: Context) -> None:
    """Check test coverage.

    Parameters
    ----------
    ctx : invoke.Context
        The invoke context object.

    Notes
    -----
    This runs tests with coverage measurement and generates an HTML
    coverage report. The report will be available in the htmlcov/
    directory and can be opened in a browser for detailed analysis.

    See Also
    --------
    https://pytest-cov.readthedocs.io/
        Documentation for pytest-cov plugin.

    """
    ctx.run(f"{PYTEST} --cov={TEST_TARGET} --cov-report=html", pty=USE_PTY)
