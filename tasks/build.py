"""Task for build.

Methods
-------
clean:
    Remove all the tmp files in `.gitignore`.
develop:
    Install environement in development mode.
dist:
    Build distribution.
install:
    Install environement in product mode.

"""
from invoke import Collection, task

from tasks import style, test
from tasks._common import VENV_PREFIX


@task
def develop(ctx):
    """Install script in pipenv environement in development mode"""
    ctx.run(f"{VENV_PREFIX} python setup.py develop")


@task
def install(ctx):
    """Install script in pipenv environement"""
    ctx.run(f"{VENV_PREFIX} python setup.py install")


@task(pre=[style.run, test.run])
def dist(ctx):
    """Build distribution"""
    ctx.run(f"{VENV_PREFIX} python setup.py sdist bdist_wheel")


@task
def clean(ctx):
    """Remove all the tmp files in `.gitignore`"""
    ctx.run("git clean -Xdf")


build_ns = Collection("build")
build_ns.add_task(develop)
build_ns.add_task(install)
build_ns.add_task(dist)
build_ns.add_task(clean)
