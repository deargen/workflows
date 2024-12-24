from os import PathLike


def get_min_python_version(
    project_dir: str | PathLike | None = None,
):
    """
    Get the minimum python version from the pyproject.toml file.
    """
    import tomllib

    from python_projector.utils.files import find_pyproject_toml
    from python_projector.utils.toml import get_toml_value
    from python_projector.utils.version import min_version_requires_python

    pyproject_toml = find_pyproject_toml(project_dir)
    with pyproject_toml.open("rb") as f:
        pyproject = tomllib.load(f)

    version_range: str = get_toml_value(
        pyproject, ["project", "requires-python"], raise_error=True
    )
    min_version = min_version_requires_python(version_range)
    return min_version


def get_src_dir(project_dir: str | PathLike | None = None):
    """
    Print the `src/` directory based on the pyproject.toml file.
    """
    from python_projector.utils.files import find_pyproject_toml, get_src_dir

    pyproject_toml = find_pyproject_toml(project_dir)
    src_directory = get_src_dir(pyproject_toml)

    return src_directory
