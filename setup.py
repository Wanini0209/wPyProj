#!/usr/bin/env python3
# pylint: disable=missing-module-docstring
from os import path

from setuptools import setup

# Project Info
DISTNAME = 'wPyProj'
VERSION = '1.0.0'

# One-line description or tagline of what the project does.
DESCRIPTION = "Wanini's Python Template Project Generator"

# Get the long description from the README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "docs/README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Project's main homepage
URL = 'https://github.com/Wanini0209/wPyProj'
DOWNLOAD_URL = 'https://github.com/Wanini0209/wPyProj.git'

# Information of author and mainatiner
AUTHOR = "Ting-Hsu Chang"
AUTHOR_EMAIL = "ting.hsu.chang@gmail.com"
MAINTAINER = "Ting-Hsu Chang"
MAINTAINER_EMAIL = "ting.hsu.chang@gmail.com"

# Information of License
LICENSE = 'MIT License'

# Classifiers help users find your project by categorizing it.
#
# For a list of valid classifiers, see https://pypi.org/classifiers/
classifiers = [
    'Operating System :: Microsoft :: Windows :: Windows 10',
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Financial and Insurance Industry',
    'Topic :: Office/Business :: Financial',

    # Pick your license as you wish
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate you support Python 3. These classifiers are *not*
    # checked by 'pip install'. See instead 'python_requires' below.
    'Programming Language :: Python :: 3.12'
    'Programming Language :: Python :: 3.13'
    'Programming Language :: Python :: 3 :: Only'
]

# This field adds keywords for your project which will appear on the
# project page. What does your project relate to?
#
# Note that this is a list of additional keywords, separated
# by commas, to be used to assist searching for the distribution in a
# larger catalog.
# for example:
#
#   keywords = 'sample, setuptools, development'
#
keywords = ['finance', 'technical analysis', 'technical indicator']

# set packages manually or use `find_packages` tool
# for example:
#
#   packages = find_packages(where='.', exclude=(), include=('*',))
#
packages = ['samples']

# Definition Python version supported
PYTHON_REQUIRES = '>=3.12, <4'

# Definition required packages
requires = []

# setup project
setup(
    name=DISTNAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=URL,
    download_url=DOWNLOAD_URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    license=LICENSE,
    classifiers=classifiers,
    keywords=keywords,
    packages=packages,
    python_requires=PYTHON_REQUIRES,
    install_requires=requires,
    include_package_data=False)
