"""Utility functions."""


def read_text(file: str, encoding: str = "utf-8") -> str:
    """Read content from text file."""
    with open(file, encoding=encoding) as src:
        ret = src.read()
    return ret


def write_text(data: str, file: str, encoding: str = "utf-8"):
    """Write content to text file."""
    with open(file, "w", encoding=encoding) as dst:
        dst.write(data)
