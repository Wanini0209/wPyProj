"""Task for document.

Methods
-------
build:
    Build documentation locally.
deploy:
    Deploy to github page.
serve:
    Run local server.

"""

from invoke import Context, task

from tasks._common import VENV_PREFIX


@task(optional=["clean"])
def build(ctx: Context, clean: bool = True) -> None:
    """Build documentation locally.

    Parameters
    ----------
    ctx : invoke.Context
        The invoke context object.
    clean : bool, optional
        Whether to clean before building, by default True.

    Notes
    -----
    This uses MkDocs to build the documentation. The output will
    be in the site/ directory.

    """
    argument = ""
    if clean:
        argument += " --clean"

    ctx.run(f"{VENV_PREFIX} mkdocs build{argument}")


@task(default=True)
def serve(ctx: Context) -> None:
    """Run local server.

    Parameters
    ----------
    ctx : invoke.Context
        The invoke context object.

    Notes
    -----
    This starts a local development server with live reloading.
    The documentation will be available at http://localhost:8000.

    """
    ctx.run(f"{VENV_PREFIX} mkdocs serve")


@task
def deploy(ctx: Context) -> None:
    """Deploy to github page.

    Parameters
    ----------
    ctx : invoke.Context
        The invoke context object.

    Notes
    -----
    This deploys the documentation to GitHub Pages. Requires proper
    repository configuration and permissions.

    """
    ctx.run(f"{VENV_PREFIX} mkdocs gh-deploy")
