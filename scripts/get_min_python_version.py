"""
Get minimum python version from pyproject.toml.

Note:
    It only works if the format is like this: ">=3.11", ">=3.11,<3.12"
"""

from __future__ import annotations

import sys
from collections.abc import Iterable
from os import PathLike
from pathlib import Path


def find_root_dir_with_file(
    source: str | PathLike, marker: str | Iterable[str]
) -> Path:
    """
    Find the first parent directory containing a specific "marker", relative to a file path.
    """
    source = Path(source).resolve()
    if isinstance(marker, str):
        marker = {marker}

    while source != source.parent:
        if any((source / m).exists() for m in marker):
            return source

        source = source.parent

    raise FileNotFoundError(f"File {marker} not found in any parent directory")


if len(sys.argv) == 2:
    pyproject_toml_path = Path(sys.argv[1])
elif len(sys.argv) == 1:
    pyproject_toml_path = (
        find_root_dir_with_file(Path.cwd(), "pyproject.toml") / "pyproject.toml"
    )
else:
    raise ValueError("Invalid number of arguments")

if not pyproject_toml_path.exists():
    raise FileNotFoundError(f"{pyproject_toml_path} not found")

try:
    import toml

    pyproject = toml.load(pyproject_toml_path)
    version_range = pyproject["project"]["requires-python"]
except (ImportError, ModuleNotFoundError):
    # alternatively, search for requires-python in pyproject.toml
    with open(pyproject_toml_path) as f:
        for line in f:
            if line.startswith("requires-python"):
                version_range = line.replace("requires-python", "").strip(" ='\"\n")
                break
        else:
            raise ValueError("requires-python not found in pyproject.toml")


# get minimum python version
# it has a format like this: ">=3.6", ">=3.7,<3.8"
min_version = version_range.split(",")[0].replace(">=", "")
print(min_version)  # noqa: T201
