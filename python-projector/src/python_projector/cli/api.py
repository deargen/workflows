import tomllib
from os import PathLike
from pathlib import Path


class InvalidConfigError(Exception):
    pass


def get_min_python_version(
    project_dir: str | PathLike | None = None,
):
    """
    Get the minimum python version from the pyproject.toml file.
    """
    import tomllib

    from python_projector.utils.files import find_pyproject_toml
    from python_projector.utils.version import min_version_requires_python

    pyproject_toml = find_pyproject_toml(project_dir)
    with pyproject_toml.open("rb") as f:
        pyproject = tomllib.load(f)

    try:
        version_range = pyproject["project"]["requires-python"]
    except KeyError as e:
        raise InvalidConfigError(
            "Missing key project.requires-python in pyproject.toml"
        ) from e
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


def get_versioneer_version(
    project_dir: str | PathLike | None = None,
    *,
    chrome_compatible: bool = False,
):
    """
    Similar to `versioneer.get_version()`, but with more options.
    """
    import versioneer

    from python_projector.utils.files import find_pyproject_toml
    from python_projector.utils.version import (
        versioneer_render_chrome_ext_compat_version,
    )

    pyproject_toml = find_pyproject_toml(project_dir)
    with pyproject_toml.open("rb") as f:
        pyproject = tomllib.load(f)

    if project_dir is None:
        project_dir = pyproject_toml.parent
    elif isinstance(project_dir, str):
        project_dir = Path(project_dir)

    try:
        tag_prefix = pyproject["tool"]["versioneer"]["tag_prefix"]  # usually "v"
    except KeyError as e:
        raise InvalidConfigError(
            f"Missing key tool.versioneer.tag_prefix in {pyproject_toml}"
        ) from e

    try:
        style = pyproject["tool"]["versioneer"]["style"]  # pep440
    except KeyError as e:
        raise InvalidConfigError(
            f"Missing key tool.versioneer.style in {pyproject_toml}"
        ) from e

    pieces = versioneer.git_pieces_from_vcs(
        tag_prefix=tag_prefix, root=project_dir, verbose=True
    )

    if chrome_compatible or style == "chrome-ext":
        version = versioneer_render_chrome_ext_compat_version(pieces=pieces)
    else:
        version = versioneer.render(pieces=pieces, style=style)["version"]

    return version
