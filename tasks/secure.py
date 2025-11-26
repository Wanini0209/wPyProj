"""Tasks for code-security.

Methods
-------
security_report:
    Check common software vulnerabilities through `ruff` with bandit rules.

"""

from invoke import Context, task


@task
def security_report(ctx: Context) -> None:
    """Run security checks using Ruff's built-in bandit rules.

    Parameters
    ----------
    ctx : invoke.Context
        The invoke context object.

    Notes
    -----
    This uses Ruff's implementation of bandit security rules to check
    for common security issues in Python code. The --select B flag
    selects only bandit rule set. The --no-fix flag is used because
    security issues typically require manual review and should not be
    automatically fixed.

    See Also
    --------
    https://docs.astral.sh/ruff/rules/#flake8-bandit-b
        Documentation of bandit rules in Ruff.

    """
    print("--- Running security scan (Bandit rules via Ruff) ---")
    # --select B selects only bandit rule set
    # --no-fix because security issues need manual review
    ctx.run("ruff check . --select B --no-fix")
