# Allow print
# Allow many arguments
# Allow relative import from parent
# ruff: noqa: T201 PLR0913 TID252
import sys
import tomllib
from pathlib import Path
from typing import Annotated

import typer

app = typer.Typer(
    no_args_is_help=True, context_settings={"help_option_names": ["-h", "--help"]}
)


class InvalidConfigError(Exception):
    pass


def version_callback(*, value: bool):
    if value:
        from .. import __version__

        print(__version__)
        raise typer.Exit


@app.callback()
def common(
    ctx: typer.Context,
    *,
    version: bool = typer.Option(
        None, "-v", "--version", callback=version_callback, help="Show version"
    ),
):
    pass


@app.command()
def find_pyproject_toml(project_dir: Annotated[Path | None, typer.Argument()] = None):
    """
    Find the pyproject.toml file in the current directory or any parent directory.
    """
    from python_projector.utils import files

    print(files.find_pyproject_toml(project_dir))


@app.command()
def get_min_python_version(
    project_dir: Annotated[Path | None, typer.Argument()] = None,
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
    print(min_version)


@app.command()
def get_src_dir(project_dir: Annotated[Path | None, typer.Argument()] = None):
    """
    Print the `src/` directory based on the pyproject.toml file.
    """
    from python_projector.utils.files import find_pyproject_toml, get_src_dir

    pyproject_toml = find_pyproject_toml(project_dir)
    src_directory = get_src_dir(pyproject_toml)

    print(src_directory)


@app.command()
def gen_init_py(project_dir: Annotated[Path | None, typer.Argument()] = None):
    """Generate __init__.py files for all subdirectories of src/."""
    from python_projector.utils.files import (
        find_pyproject_toml,
        gen_init_py,
        get_src_dir,
    )

    pyproject_toml = find_pyproject_toml(project_dir)
    src_directory = get_src_dir(pyproject_toml)

    gen_init_py(src_directory)


@app.command()
def pip_compile(project_dir: Annotated[Path | None, typer.Argument()] = None):
    """Generate requirements.txt and requirements-dev.txt files."""
    from python_projector import __file__ as python_projector_file
    from python_projector.utils.files import (
        find_pyproject_toml,
    )
    from python_projector.utils.version import min_version_requires_python

    pip_compile_shell_file = (
        Path(python_projector_file).parent / "shell" / "pip_compile.sh"
    )

    # ```toml
    # [tool.projector.pip_compile]
    # requirements_in_dir = "deps"
    # requirements_out_dir = "deps/lock"
    # python_platforms = ["x86_64-manylinux_2_28", "aarch64-apple-darwin", "x86_64-apple-darwin"]
    # ```
    pyproject_toml = find_pyproject_toml(project_dir)
    with pyproject_toml.open("rb") as f:
        pyproject = tomllib.load(f)

    try:
        requirements_in_dir = pyproject["tool"]["projector"]["pip_compile"][
            "requirements_in_dir"
        ]
    except KeyError as e:
        raise InvalidConfigError(
            "Missing key tool.projector.pip_compile.requirements_in_dir in pyproject.toml"
        ) from e

    try:
        requirements_out_dir = pyproject["tool"]["projector"]["pip_compile"][
            "requirements_out_dir"
        ]
    except KeyError as e:
        raise InvalidConfigError(
            "Missing key tool.projector.pip_compile.requirements_out_dir in pyproject.toml"
        ) from e

    try:
        python_platforms = pyproject["tool"]["projector"]["pip_compile"][
            "python_platforms"
        ]
    except KeyError as e:
        raise InvalidConfigError(
            "Missing key tool.projector.pip_compile.python_platforms in pyproject.toml"
        ) from e

    try:
        version_range = pyproject["project"]["requires-python"]
    except KeyError as e:
        raise InvalidConfigError(
            "Missing key project.requires-python in pyproject.toml"
        ) from e

    requirements_in_dir = pyproject_toml.parent / requirements_in_dir
    requirements_out_dir = pyproject_toml.parent / requirements_out_dir
    min_version = min_version_requires_python(version_range)
    python_platforms = ",".join(python_platforms)

    # Run the shell script
    import subprocess

    ps = subprocess.run(
        [
            "bash",
            str(pip_compile_shell_file),
            requirements_in_dir,
            requirements_out_dir,
            min_version,
            python_platforms,
        ],
        check=False,
    )

    sys.exit(ps.returncode)


@app.command()
def run_doctest(project_dir: Annotated[Path | None, typer.Argument()] = None):
    """
    Run doctest for all modules in `src/` directory.

    It will run all modules in `src/` directory and print the result of doctest.

    It also has to load all modules in `src/` directory, so it will run all modules and test if they can be imported.
    So if any module doesn't run (e.g. syntax error, import error, etc.), it will also fail.
    """
    from python_projector.utils.files import find_pyproject_toml, get_src_dir
    from python_projector.utils.tests import run_doctest

    pyproject_toml = find_pyproject_toml(project_dir)
    src_directory = get_src_dir(pyproject_toml)

    (
        num_modules_with_doctest,
        num_attempted,
        num_failed,
        failed_modules,
    ) = run_doctest(src_directory)

    print()
    if num_failed == 0:
        print(
            f"✅ All {num_attempted} tests passed in {num_modules_with_doctest} modules."
        )
    else:
        print("All failed modules:")
        for failed_module in failed_modules:
            print(f"  - {failed_module}")
        print(
            f"🚨 {num_failed} failed out of {num_attempted} tests in {num_modules_with_doctest} modules."
        )
        sys.exit(1)


def main():
    app()


if __name__ == "__main__":
    main()
