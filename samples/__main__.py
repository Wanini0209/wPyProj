# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 11:50:00 2022

@author: Ting-Hsu Chang
@email: Wanini.KLP.Mashimaro@gmail.com
"""

import os
import re

from _libs import ProjectInfo, gen_project  # pylint: disable=import-error

# receive the path of this project.
while True:
    path = input("Please input the path of this project: ")
    if not os.path.exists(path):
        print(f"No such file or directory: '{path}'")
        continue
    break

# receive the Github url of this project

GITHUB_URL_PAT = re.compile(r'https://github.com/'
                            r'[a-zA-Z_]+[a-zA-Z0-9\-_]*/'
                            r'[a-zA-Z_]+[a-zA-Z0-9\-_]*')
while True:
    url = input("Please input the Github url of this project: ")
    if not GITHUB_URL_PAT.match(url):
        print(f"illegal Github url: '{url}'")
        continue
    break

# receive the name of this project
PROJECT_NAME_PAT = re.compile(r'[a-zA-Z]+[a-zA-Z0-9\-_]*')
name = input("Please input the name of this project: ")
if not PROJECT_NAME_PAT.match(name):
    raise ValueError(f"illegal project name: '{name}'")

# receive the One-line description of this project
while True:
    description = input("Please input the One-line description of this project: ")
    if '\n' in description:
        print(f"illegal One-line description: '{description}'")
        continue
    break

# receive the package name of this project
LIB_NAME_PAT = re.compile('[a-z]+[a-z0-9_]*')
while True:
    package = input("Please input the package name of this project: ")
    if not LIB_NAME_PAT.match(package):
        print(f"illegal package name: '{package}'")
        continue
    break

# receive the author of this project
author = input("Please input the name of author of this project: ")

# receive the author email of this project
EMAIL_PAT = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
while True:
    email = input("Please input the email of author of this project: ")
    if not EMAIL_PAT.match(email):
        print(f"illegal email: '{email}'")
        continue
    break

# receive the python version of this project
PYTHON_VERSION_PAT = re.compile(r'3(\.[1-9]+0?){1,2}')
while True:
    version = input("Please input the version of Python of this project: ")
    if not PYTHON_VERSION_PAT.match(version):
        print(f"illegal Python version: '{version}'")
        continue
    break

info = ProjectInfo(path=path, url=url, name=name, description=description,
                   package=package, author=author, email=email, version=version)
gen_project(info)
