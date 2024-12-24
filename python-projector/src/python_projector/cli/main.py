# Allow print
# Allow many arguments
# Allow relative import from parent
# ruff: noqa: T201 PLR0913 TID252
import json
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Annotated, Any

import typer

from python_projector import SCRIPTS_DIR

app = typer.Typer(
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
    rich_markup_mode="rich",
)


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
    from . import api

    print(api.get_min_python_version(project_dir))


@app.command()
def get_src_dir(project_dir: Annotated[Path | None, typer.Argument()] = None):
    """
    Print the `src/` directory based on the pyproject.toml file.
    """
    from . import api

    print(api.get_src_dir(project_dir))


@app.command()
def gen_init_py(project_dir: Annotated[Path | None, typer.Argument()] = None):
    """Generate __init__.py files for all subdirectories of src/."""
    from python_projector.utils.files import (
        find_pyproject_toml,
    )

    pyproject_toml = find_pyproject_toml(project_dir)
    project_dir = pyproject_toml.parent

    ps = subprocess.run(
        [
            "ruff",
            "check",
            "--select",
            "INP001",
            "--output-format",
            "json",
            project_dir,
        ],
        check=False,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )

    # https://docs.astral.sh/ruff/linter/#exit-codes
    if ps.returncode == 2:
        print("❌ Failed to run `ruff check --select INP001`.")
        sys.exit(ps.returncode)

    ruff_errors: list[dict[str, Any]] = json.loads(ps.stdout)

    generated_dirs: set[Path] = set()
    for error in ruff_errors:
        generated_dirs.add(Path(error["filename"]).parent)

    for generated_dir in generated_dirs:
        (generated_dir / "__init__.py").touch()

    if not generated_dirs:
        print("👍 No directories found with missing __init__.py files.")
    else:
        print("✅ Generated __init__.py files for the following directories:")
        for generated_dir in generated_dirs:
            print(f"  - {generated_dir}")


@app.command()
def pip_compile(project_dir: Annotated[Path | None, typer.Argument()] = None):
    r"""
    Generate requirements*.txt files from requirements*.in.

    The pyproject.toml should have the following configuration:

    ```toml
    \[tool.projector.pip-compile]
    requirements-in-dir = "deps"
    requirements-out-dir = "deps/lock"
    python-platforms = ["x86_64-manylinux_2_28", "aarch64-apple-darwin", "x86_64-apple-darwin"]
    ```
    """
    from python_projector.utils.files import (
        find_pyproject_toml,
    )
    from python_projector.utils.toml import get_toml_value
    from python_projector.utils.version import min_version_requires_python

    pip_compile_shell_file = SCRIPTS_DIR / "pip_compile.sh"

    pyproject_toml = find_pyproject_toml(project_dir)
    with pyproject_toml.open("rb") as f:
        pyproject = tomllib.load(f)

    try:
        requirements_in_dir = get_toml_value(
            pyproject,
            ["tool", "projector", "pip_compile", "requirements_in_dir"],
            raise_error=True,
        )
        requirements_out_dir = get_toml_value(
            pyproject,
            ["tool", "projector", "pip_compile", "requirements_out_dir"],
            raise_error=True,
        )
        python_platforms = get_toml_value(
            pyproject,
            ["tool", "projector", "pip_compile", "python_platforms"],
            raise_error=True,
        )
        print(
            "Please update your pyproject.toml [tool.projector.pip_compile] section to "
            "[tool.projector.pip-compile] (use hyphen instead)"
        )
        print("Please change requirements_in_dir to requirements-in-dir")
        print("Please change requirements_out_dir to requirements-out-dir")
        print("Please change python_platforms to python-platforms")
    except KeyError:
        requirements_in_dir = get_toml_value(
            pyproject,
            ["tool", "projector", "pip-compile", "requirements-in-dir"],
            raise_error=True,
        )
        requirements_out_dir = get_toml_value(
            pyproject,
            ["tool", "projector", "pip-compile", "requirements-out-dir"],
            raise_error=True,
        )
        python_platforms = get_toml_value(
            pyproject,
            ["tool", "projector", "pip-compile", "python-platforms"],
            raise_error=True,
        )

    version_range: str = get_toml_value(
        pyproject, ["project", "requires-python"], raise_error=True
    )

    requirements_in_dir = pyproject_toml.parent / requirements_in_dir
    requirements_out_dir = pyproject_toml.parent / requirements_out_dir
    min_version = min_version_requires_python(version_range)
    python_platforms = ",".join(python_platforms)

    # Run the shell script
    ps = subprocess.run(
        [
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

    pyproject_toml = find_pyproject_toml(project_dir)
    src_directory = get_src_dir(pyproject_toml)

    # it needs to be run with subprocess.run to avoid ModuleNotFoundError
    # because python-projector may not be installed in the current python environment
    # and it is supposed to be a CLI tool
    ps = subprocess.run(
        [
            SCRIPTS_DIR / "run_doctest.py",
            src_directory,
        ],
        check=False,
    )

    sys.exit(ps.returncode)


def main():
    app()


if __name__ == "__main__":
    main()
