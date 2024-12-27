import tomllib
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


def find_pyproject_toml(project_dir: str | PathLike | None = None) -> Path:
    """
    Find the pyproject.toml file in the current directory or any parent directory.
    """
    if project_dir is None:
        project_dir = Path.cwd()
    return find_root_dir_with_file(project_dir, "pyproject.toml") / "pyproject.toml"


def get_src_dir(pyproject_toml_path: str | PathLike | None) -> Path:
    if pyproject_toml_path is None:
        pyproject_toml_path = find_pyproject_toml()

    with open(pyproject_toml_path, "rb") as f:
        pyproject = tomllib.load(f)

    try:
        # 1. try setuptools
        src_directory = Path(
            pyproject["tool"]["setuptools"]["find-directories"]["where"]
        )
    except KeyError as e:
        try:
            # 2. try hatchling
            # [tool.hatch.build.targets.wheel]
            # sources = ["src"]
            src_directories = pyproject["tool"]["hatch"]["build"]["targets"]["wheel"][
                "sources"
            ]
        except KeyError as e:
            # 3. default is src/
            src_directory = Path(pyproject_toml_path).parent / "src"
            if not src_directory.exists():
                raise KeyError(
                    "Missing key tool.setuptools.find-directories.where in pyproject.toml"
                ) from e
        else:
            if isinstance(src_directories, list):
                if len(src_directories) > 1:
                    raise KeyError(
                        "Multiple source directories found in pyproject.toml. Not supported."
                    ) from e
                else:
                    src_directory = Path(src_directories[0])
            elif isinstance(src_directories, str):
                src_directory = Path(src_directories)
            else:
                raise KeyError(
                    "Invalid source directory found in pyproject.toml. Not supported."
                ) from e
    return src_directory.resolve()
