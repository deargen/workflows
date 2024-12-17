"""
Automatically generate __init__.py files for all subdirectories.

Useful before building mkdocs documentation.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def gen_init_py(project_dir: Path | None = None):
    if project_dir is None:
        project_dir = Path.cwd()

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


def main():
    if len(sys.argv) == 2:
        project_dir = Path(sys.argv[1])
    elif len(sys.argv) == 1:
        project_dir = None
    else:
        print("Usage: python gen_init_py.py [project_dir]")
        sys.exit(1)

    gen_init_py(project_dir)


if __name__ == "__main__":
    main()
