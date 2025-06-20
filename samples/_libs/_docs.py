# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 14:05:00 2022

@author: Ting-Hsu Chang
@email: Wanini.KLP.Mashimaro@gmail.com
"""

import os

from ._common import ProjectInfo
from ._utils import write_text


def _contributing(info: ProjectInfo) -> str:
    """Content-Generator for `_contributing.md` file."""
    ret = ("## Contributing\n\n"
           "### Step 1. Fork this repository to your GitHub\n\n"
           "### Step 2. Clone the repository from your GitHub\n\n"
           "```sh\ngit clone https://github.com/[YOUR GITHUB ACCOUNT]/"
           f"{info.name}.git\n```\n\n"
           "### Step 3. Add this repository to the remote in your local repository\n\n"
           f"```sh\ngit remote add upstream \"{info.url}\"\n```\n\n"
           "You can pull the latest code in master branch through "
           "`git pull upstream master` afterward.\n\n"
           "### Step 4. Check out a branch for your new feature\n\n"
           "```sh\ngit checkout -b [YOUR FEATURE]\n```\n\n"
           "### Step 5. Install Prerequsite\n\n"
           "```sh\npython -m pip install pipx\n"
           "python -m pipx install pipenv invoke\n"
           "python -m pipx ensurepath\n```\n\n"
           "### Step 6. Create Your Own Python Virtual Environment "
           "and Install Depdencies\n\n"
           "```sh\ninv env.init-dev\n```\n\n"
           "### Step 6. Work on your new feature\n\n"
           "### [Optional] Step 7. Install Attendees Analyzer for local test\n\n"
           "If you want to develop it, please run:\n\n"
           "```sh\ninv build.develop\n```\n\n"
           "### Step 8. Run test cases\n\n"
           "Make sure all test cases pass.\n\n"
           "```sh\ninv test\n```\n\n"
           "### Step 9. Run test coverage\n\n"
           "Check the test coverage and see where you can add test cases.\n\n"
           "```sh\ninv test.cov\n```\n\n"
           "### Step 10. Reformat source code\n\n"
           "Format your code through `black` and `isort`.\n\n"
           "```sh\ninv style.reformat\n```\n\n"
           "### Step 11. Run style check\n\n"
           "Make sure your coding style passes all enforced linters.\n\n"
           "```sh\ninv style\n```\n\n"
           "[Optional] Check your coding style through `pylint`. "
           "Note that you do not have to fix all the issues warned by `pylint`.\n\n"
           "```sh\ninv style.pylint\n```\n\n"
           "### [Optional] Step 12. Run security check\n\n"
           "Ensure the packages installed are secure\n\n"
           "```sh\ninv secure\n```\n\n"
           "*[Optional]* Check whether there is common security issue in the code. "
           "Note that you do not have to fix all the issues warned by `bandit`\n\n"
           "```sh\ninv secure.bandit\n```\n\n"
           "### [Optional] Develop on Conda Environment\n\n"
           "Generate requirements via `pip freeze`\n\n"
           "```sh\ninv conda.freeze\n```\n\n"
           "Create Conda develope environment\n\n"
           "```sh\ninv conda.create\n```\n\n"
           "Remove Conda develope environment\n\n"
           "```sh\ninv conda.remove\n```\n\n"
           "Activate Conda develope environment\n\n"
           "```sh\ninv conda.activate\n```\n")
    return ret


def _readme(info: ProjectInfo) -> str:
    """Content-Generator for `READMe.md` file."""
    ret = (f"# {info.description} ({info.name})\n\n"
           "## Prerequsite\n\n"
           "### Use pipx\n"
           f"* [Python {info.version}](https://www.python.org/downloads/)\n"
           "* [pipx](https://github.com/pipxproject/pipx): "
           "(Optional)for python tool management\n"
           "    - python -m pip install --user pipx\n"
           "    - python -m pipx ensurepath\n"
           "* [pipenv](https://github.com/pypa/pipenv): for dependency management\n"
           "    - python -m pipx install pipenv\n"
           "* [invoke](https://github.com/pyinvoke/invoke): for task management\n"
           "    - python -m pipx install invoke\n\n"
           "### Use Anconda\n"
           "* [MiniConda](https://repo.anaconda.com/miniconda/"
           "Miniconda3-latest-Windows-x86_64.exe)\n"
           "* [pipenv](https://github.com/pypa/pipenv): for dependency management\n"
           "    - python -m pip install pipenv\n"
           "* [invoke](https://github.com/pyinvoke/invoke): for task management\n"
           "    - python -m pip install invoke\n\n"
           "## Installation\n\n"
           f"```sh\npython -m pip install {info.name}\n```\n\n"
           "## Contributing\n"
           "Please see the [Contributing](contributing.md) for further details.\n")
    return ret


_CHANGE_LOG = (
    "# Changelog\n\n"
    "All notable changes to this project will be documented in this file."
    "\n\n"
    "The format is based on [Keep a Changelog]"
    "(https://keepachangelog.com/en/1.0.0/),\n"
    "and this project adheres to [Semantic Versioning]"
    "(https://semver.org/spec/v2.0.0.html).\n\n"
    "## [Unreleased]\n\n"
    "### Added\n")


def gen_docs(info: ProjectInfo):
    """Content-Generator for documents."""
    write_text(_CHANGE_LOG, f'{info.path}/{info.name}/CHANGELOG.md')
    path = f'{info.path}/{info.name}/docs'
    os.makedirs(path)
    write_text(_contributing(info), f'{path}/contributing.md')
    write_text(_readme(info), f'{path}/README.md')
