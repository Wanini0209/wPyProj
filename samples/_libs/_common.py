"""Common definitions and ProjectInfo class."""

import json
from typing import NamedTuple


class ProjectInfo(NamedTuple):
    """Project Information."""

    path: str
    url: str
    name: str
    description: str
    package: str
    author: str
    email: str
    version: str

    def to_dict(self) -> dict[str, str]:
        """Convert to dictionary."""
        ret = {
            "path": self.path,
            "url": self.url,
            "name": self.name,
            "description": self.description,
            "package": self.package,
            "author": self.author,
            "email": self.email,
            "version": self.version,
        }
        return ret

    def dump2json(self, file: str):
        """Dump to JSON file."""
        with open(file, "w", encoding="utf-8") as fout:
            json.dump(self.to_dict(), fout)

    @classmethod
    def from_dict(cls, recv: dict[str, str]) -> "ProjectInfo":
        """Create from dictionary."""
        return cls(**recv)

    @classmethod
    def load4json(cls, file: str) -> "ProjectInfo":
        """Load from JSON file."""
        with open(file, encoding="utf-8") as fin:
            recv = json.load(fin)
        return cls.from_dict(recv)
