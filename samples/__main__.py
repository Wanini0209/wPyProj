"""Main entry point of the project."""

import os
import re
import sys
from collections.abc import Callable

from _libs import ProjectInfo, gen_project


def _get_input(
    prompt: str,
    validator: Callable[[str], bool] | None = None,
    error_msg: str = "Invalid input.",
    warning_check: Callable[[str], bool] | None = None,
    warning_msg: str = "",
) -> str:
    """Get and validate user input."""
    while True:
        value = input(prompt).strip()
        if not value:
            print("Input cannot be empty.")
            continue

        if validator and not validator(value):
            print(error_msg)
            continue

        if warning_check and not warning_check(value):
            print(warning_msg)
            confirm = input("Are you sure? (y/n): ")
            if confirm.lower() != "y":
                continue

        return value


def _validate_path(path: str) -> bool:
    """Validate if parent directory exists."""
    abs_path = os.path.abspath(path)
    parent_dir = os.path.dirname(abs_path)
    if not os.path.exists(parent_dir):
        print(f"Parent directory does not exist: '{parent_dir}'")
        return False
    return True


def main():
    """Run the project generator."""
    # 1. Path
    path_input = _get_input(
        "Please input the path where to create the project: ",
        validator=_validate_path,
    )
    path = os.path.abspath(path_input)

    # 2. URL
    url = _get_input(
        "Please input the Repository URL (e.g. GitHub url): ",
        warning_check=lambda x: "http" in x or "git@" in x,
        warning_msg="Warning: input does not look like a standard URL.",
    )

    # 3. Project Name
    name_pat = re.compile(r"^[a-zA-Z]+[a-zA-Z0-9\-_]*$")
    name = _get_input(
        "Please input the name of this project: ",
        validator=lambda x: bool(name_pat.match(x)),
        error_msg=(
            "Illegal project name. Name must start with a letter and "
            "contain only letters, numbers, '-', or '_'."
        ),
    )

    # 4. Description
    description = _get_input(
        "Please input the One-line description of this project: ",
        validator=lambda x: "\n" not in x,
        error_msg="Illegal One-line description.",
    )

    # 5. Package Name
    lib_pat = re.compile(r"^[a-z]+[a-z0-9_]*$")
    package = _get_input(
        "Please input the package name (import name) of this project: ",
        validator=lambda x: bool(lib_pat.match(x)),
        error_msg="Illegal package name. Must be lowercase.",
    )

    # 6. Author
    author = _get_input("Please input the name of author of this project: ")

    # 7. Email
    email_pat = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    email = _get_input(
        "Please input the email of author of this project: ",
        validator=lambda x: bool(email_pat.match(x)),
        error_msg="Illegal email format.",
    )

    # 8. Version
    ver_pat = re.compile(r"3(\.[1-9]+0?){1,2}")
    version = _get_input(
        "Please input the version of Python of this project (e.g. 3.12): ",
        validator=lambda x: bool(ver_pat.match(x)),
        error_msg="Illegal Python version (e.g., 3.12).",
    )

    info = ProjectInfo(
        path=path,
        url=url,
        name=name,
        description=description,
        package=package,
        author=author,
        email=email,
        version=version,
    )
    gen_project(info)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled by user.")
        sys.exit(1)
