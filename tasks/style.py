"""Tasks for code-style.

Methods
-------
check:
    Run static analysis and formatting checks without modifying files.
format:
    Automatically format code and fix linting issues.
style:
    Default task, executes all automatic formatting and fixes.
run:
    Alias for style task (for backward compatibility).

"""

from invoke import Context, task

from tasks._common import VENV_PREFIX


@task
def check(ctx: Context) -> None:
    """Run static analysis and formatting checks without modifying files.

    Parameters
    ----------
    ctx : invoke.Context
        The invoke context object.

    Notes
    -----
    This task is suitable for CI/CD pipelines where you want to verify
    code style without making changes. It will report any style violations
    but won't modify any files.

    """
    print("--- Checking format: Black ---")
    ctx.run(f"{VENV_PREFIX} black --check .", warn=True)

    print("\n--- Code checking: Ruff ---")
    ctx.run(f"{VENV_PREFIX} ruff check .", warn=True)


@task
def format(ctx: Context) -> None:
    """Automatically format code and fix linting issues.

    Parameters
    ----------
    ctx : invoke.Context
        The invoke context object.

    Notes
    -----
    This task is for local development use. It will automatically:
    - Format code using Black
    - Fix linting issues using Ruff where possible

    """
    print("--- Auto-formatting: Black ---")
    ctx.run(f"{VENV_PREFIX} black .")

    print("\n--- Auto-fixing: Ruff ---")
    ctx.run(f"{VENV_PREFIX} ruff check . --fix")


@task(pre=[format], default=True)
def style(ctx: Context) -> None:
    """Execute all automatic formatting and fixes.

    Parameters
    ----------
    ctx : invoke.Context
        The invoke context object.

    Notes
    -----
    This is the default task for the style collection. It runs all
    formatting and fixing operations to ensure code style compliance.

    """
    print("\n[OK] Code style has been automatically fixed and synchronized.")


@task(pre=[format])
def run(ctx: Context) -> None:
    """Run style task (alias for backward compatibility).

    Parameters
    ----------
    ctx : invoke.Context
        The invoke context object.

    Notes
    -----
    This task exists for backward compatibility with code that expects
    a 'run' task in the style module. It performs the same operations
    as the 'style' task.

    """
    print("\n[OK] Code style has been automatically fixed and synchronized.")
