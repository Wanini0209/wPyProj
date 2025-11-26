"""Configuration file generators."""

import shutil

from ._common import ProjectInfo
from ._utils import write_text


def mkdocs(info: ProjectInfo) -> str:
    """Content-Generator for `mkdocs.yml` file."""
    ret = (
        f"site_name: {info.description}\n"
        "nav:\n"
        "    - Home: README.md\n"
        "    - Contributing: contributing.md\n\n"
        f"repo_url: {info.url}\n"
        "remote_branch: gh-pages\n"
        "remote_name: origin\n"
    )
    return ret


def pyproject_toml(info: ProjectInfo) -> str:
    """Content-Generator for `pyproject.toml` file."""
    # 動態計算 Python 版本格式 (例如: 3.12 -> py312)
    # 取版本號的前兩部分 (Major.Minor)，去除小數點並加上 py 前綴
    py_ver_str = "".join(info.version.split(".")[:2])
    target_ver = f"py{py_ver_str}"

    ret = (
        "[tool.black]\n"
        "line-length = 88\n"
        f"target-version = ['{target_ver}']\n\n"
        "[tool.ruff]\n"
        "# 設定 ruff 的行為，使其與 black 相容\n"
        "line-length = 88\n"
        f'target-version = "{target_ver}"\n\n'
        "[tool.ruff.lint]\n"
        "# 選擇要啟用的規則集\n"
        "# 'E', 'F' - flake8 預設規則\n"
        "# 'W' - pycodestyle 警告\n"
        "# 'I' - isort (導入排序)\n"
        "# 'D' - pydocstyle (文件字串風格)\n"
        "# 'B' - bandit (安全性)\n"
        "# 'C4' - flake8-comprehensions\n"
        "# 'UP' - pyupgrade\n"
        "# 'PL' - pylint\n"
        'select = ["E", "F", "W", "I", "D", "B", "C4", "UP", "PL"]\n\n'
        "# 可以忽略特定的規則\n"
        'ignore = ["D100", "D104", "D107", "D401"]\n\n'
        "[tool.ruff.lint.pydocstyle]\n"
        "# 設定 pydocstyle 規則，使其遵循 NumPy 風格\n"
        'convention = "numpy"\n\n'
        "[tool.ruff.lint.flake8-bandit]\n"
        "# 不需要額外設定，使用預設值即可，或根據需求新增 skips\n\n"
        "[tool.mypy]\n"
        f'files = ["{info.package}"]\n'
        "ignore_missing_imports = true\n"
        'follow_imports = "silent"\n'
        "warn_redundant_casts = true\n"
        "warn_unused_ignores = true\n"
        "warn_unused_configs = true\n"
    )
    return ret


def setup_py(info: ProjectInfo) -> str:
    """Content-Generator for `setup.py` file."""
    ret = (
        "#!/usr/bin/env python3\n"
        "# pylint: disable=missing-module-docstring\n"
        "from os import path\n\n"
        "from setuptools import setup\n\n"
        "# Project Info\n"
        f'DISTNAME = "{info.name}"\n'
        "VERSION = '1.0.0'\n\n"
        "# One-line description or tagline of what the project does.\n"
        f'DESCRIPTION = "{info.description}"\n\n'
        "# Get the long description from the README file\n"
        "this_directory = path.abspath(path.dirname(__file__))\n"
        "with open(path.join(this_directory, "
        "'README.md'), encoding='utf-8') as f:\n"
        "    long_description = f.read()\n\n"
        "# Project's main homepage\n"
        f"URL = '{info.url}'\n"
        f"DOWNLOAD_URL = '{info.url}.git'\n\n"
        "# Information of author and maintainer\n"
        f"AUTHOR = '{info.author}'\n"
        f"AUTHOR_EMAIL = '{info.email}'\n"
        f"MAINTAINER = '{info.author}'\n"
        f"MAINTAINER_EMAIL = '{info.email}'\n\n"
        "# Information of License\n"
        "LICENSE = 'MIT License'\n\n"
        "# Classifiers help users find your project by categorizing it.\n"
        "#\n"
        "# For a list of valid classifiers, see https://pypi.org/classifiers/\n"
        "classifiers = [\n"
        "    'Operating System :: Microsoft :: Windows :: Windows 10',\n"
        "    # How mature is this project? Common values are\n"
        "    #   3 - Alpha\n"
        "    #   4 - Beta\n"
        "    #   5 - Production/Stable\n"
        "    'Development Status :: 3 - Alpha',\n\n"
        "    # Indicate who your project is intended for\n"
        "    'Intended Audience :: Financial and Insurance Industry',\n"
        "    'Topic :: Office/Business :: Financial',\n\n"
        "    # Pick your license as you wish\n"
        "    'License :: OSI Approved :: MIT License',\n\n"
        "    # Specify the Python versions you support here. In particular, ensure\n"
        "    # that you indicate you support Python 3. These classifiers are *not*\n"
        "    # checked by 'pip install'. See instead 'python_requires' below.\n"
        "    'Programming Language :: Python :: 3.12',\n"
        "    'Programming Language :: Python :: 3.13',\n"
        "    'Programming Language :: Python :: 3 :: Only'\n"
        "]\n\n"
        "# This field adds keywords for your project which will appear on the\n"
        "# project page. What does your project relate to?\n"
        "#\n"
        "# Note that this is a list of additional keywords, separated\n"
        "# by commas, to be used to assist searching for the distribution in a\n"
        "# larger catalog.\n"
        "# for example:\n"
        "#\n"
        "#   keywords = 'sample, setuptools, development'\n"
        "#\n"
        "keywords = []\n\n"
        "# set packages manually or use `find_packages` tool\n"
        "# for example:\n"
        "#\n"
        "#   packages = find_packages(where='.', exclude=(), include=('*',))\n"
        "#\n"
        f"packages = ['{info.package}']\n\n"
        "# Definition Python version supported\n"
        f"PYTHON_REQUIRES = '>={info.version}, <4'\n\n"
        "# Definition required packages\n"
        "requires = []\n\n"
        "# setup project\n"
        "setup(\n"
        "    name=DISTNAME,\n"
        "    version=VERSION,\n"
        "    description=DESCRIPTION,\n"
        "    long_description=long_description,\n"
        "    long_description_content_type='text/markdown',\n"
        "    url=URL,\n"
        "    download_url=DOWNLOAD_URL,\n"
        "    author=AUTHOR,\n"
        "    author_email=AUTHOR_EMAIL,\n"
        "    maintainer=MAINTAINER,\n"
        "    maintainer_email=MAINTAINER_EMAIL,\n"
        "    license=LICENSE,\n"
        "    classifiers=classifiers,\n"
        "    keywords=keywords,\n"
        "    packages=packages,\n"
        "    python_requires=PYTHON_REQUIRES,\n"
        "    install_requires=requires,\n"
        "    include_package_data=False)\n"
    )
    return ret


def pipfile(info: ProjectInfo) -> str:
    """Content-Generator for `pipfile` file."""
    ret = (
        '[[source]]\nurl = "https://pypi.org/simple"\n'
        "verify_ssl = true\n"
        'name = "pypi"\n\n'
        "[packages]\n\n"
        "[dev-packages]\n"
        'mypy = "*"\n'
        'pytest = "*"\n'
        'pytest-cov = "*"\n'
        'pre-commit = "*"\n'
        'commitizen = "*"\n'
        'invoke = "*"\n'
        'mkdocs = "*"\n'
        'black = "*"\n'
        'ruff = "*"\n\n'
        "[requires]\n"
        f'python_version = "{info.version}"\n'
    )
    return ret


# 注意：pyproject.toml 已從這裡移除，因為現在由函數動態生成
_COPY_FILES = [".editorconfig", ".gitignore", ".pre-commit-config.yaml", "pytest.ini"]


def gen_configs(info: ProjectInfo):
    """Content-Generator for config files."""
    path = f"{info.path}/{info.name}"
    for file in _COPY_FILES:
        shutil.copyfile(file, f"{path}/{file}")

    # 使用新函數生成 pyproject.toml，不再複製靜態檔案
    write_text(pyproject_toml(info), f"{path}/pyproject.toml")

    write_text(mkdocs(info), f"{path}/mkdocs.yml")
    # 移除 setup.cfg 生成
    # write_text(setup_cfg(info), f'{path}/setup.cfg')
    write_text(setup_py(info), f"{path}/setup.py")
    write_text(pipfile(info), f"{path}/Pipfile")
