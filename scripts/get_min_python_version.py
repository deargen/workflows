"""
Get minimum python version from pyproject.toml.

Note:
    It only works if the format is like this: ">=3.11", ">=3.11,<3.12"
"""

import sys
from pathlib import Path

# pyproject_toml_path = Path(__file__).parent.parent / "pyproject.toml"

if len(sys.argv) == 2:
    pyproject_toml_path = sys.argv[1]
elif len(sys.argv) == 1:
    pyproject_toml_path = Path(__file__).parent.parent / "pyproject.toml"
else:
    raise ValueError("Invalid number of arguments")

try:
    import toml

    pyproject = toml.load(pyproject_toml_path)
    version_range = pyproject["project"]["requires-python"]
except ImportError:
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
