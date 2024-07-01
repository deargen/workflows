"""
Automatically generate __init__.py files for all subdirectories.

Useful before building mkdocs documentation.
"""
# flake8: noqa: T201

import os
import sys
from os import PathLike
from pathlib import Path


def gen_init_py(path: str | PathLike):
    """Generate __init__.py files for all subdirectories of path."""
    for root, _, files in os.walk(path):
        if "__init__.py" in files:
            continue
        if Path(root).samefile(path):
            continue
        if "__pycache__" in root:
            continue
        if root.endswith(".egg-info"):
            continue

        with open(Path(root) / "__init__.py", "w") as f:
            print("Generating __init__.py in", root)
            f.write("")


if __name__ == "__main__":
    src_dir = (
        Path(__file__).parent.parent / "src" if len(sys.argv) == 1 else sys.argv[1]
    )
    gen_init_py(src_dir)
