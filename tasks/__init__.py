"""Command for tasks.

Tasks
-----
build:
    Tasks for build.
doc:
    Task for document.
env:
    Task for environment.
git:
    Tasks for `git`.
test:
    Tasks for test.
secure:
    Tasks for code-security.
style:
    Tasks for code-style.

[Optional]
conda:
    Tasks for conda develop environment.

See Also
--------
Use `inv --list` command to list all available commands.

"""
from invoke import Collection

from tasks import conda, doc, env, git, secure, style, test
from tasks.build import build_ns

ns = Collection()
ns.add_collection(env)
ns.add_collection(git)
ns.add_collection(test)
ns.add_collection(style)
ns.add_collection(build_ns)
ns.add_collection(doc)
ns.add_collection(secure)
ns.add_collection(conda)
