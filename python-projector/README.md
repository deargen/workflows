# python-projector: A collection of simple scripts to manage Python projects

|  |  |
|--|--|
|[![Ruff](https://img.shields.io/badge/Ruff-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://github.com/astral-sh/ruff) |[![Actions status](https://github.com/deargen/workflows/workflows/%28not%20reusable%29%20Style%20checking/badge.svg)](https://github.com/deargen/workflows/actions)|
| [![Ruff](https://img.shields.io/badge/Ruff-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://github.com/astral-sh/ruff) | [![Actions status](https://github.com/deargen/workflows/workflows/%28not%20reusable%29%20Linting/badge.svg)](https://github.com/deargen/workflows/actions) |
| [![uv](https://img.shields.io/badge/uv-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://github.com/astral-sh/uv) | [![Actions status](https://github.com/deargen/workflows/workflows/%28not%20reusable%29%20Check%20pip%20compile%20sync/badge.svg)](https://github.com/deargen/workflows/actions) |

## 🛠️ Installation
```sh
# install with pip
pip install python-projector

# install with uv tool
uv tool install python-projector
```

## 🚀 Usage

### Find nearest `pyproject.toml` file with `projector find-pyproject-toml`

It will find the nearest `pyproject.toml` file in the current directory or its parent directories.

### Get src/ directory with `projector get-src-dir`

It will read the `pyproject.toml`'s `tool.setuptools.packages.find.where` setting.
If the configuration is not found, it will assume `src/` as the default value.

```toml
[tool.setuptools.packages.find]
where = ["src"]
```

### Apply `uv pip compile` with `projector pip-compile`

**Background:**

- `uv pip compile` is a command that generates a `requirements.txt` file from a `requirements.in` file.
- `requirements.in` file should contain the direct dependencies of the project, with dynamic versions.
- `requirements.txt` file contains all dependencies with pinned versions.
- This is a thin wrapper around the command to generate `requirements.txt` files per architecture.
- There exists `--universal` flag to generate a universal `requirements.txt` file, but we don't use it. Instead, we just separate the files per architecture.
    - This is because it makes the requirements overly complicated to read and parse.
- There exists a better format called `uv.lock` but this is also more complicated to read and parse.
- For now, we stick to the `requirements.txt` format for the sake of simplicity.

**Usage:**

First, configure in the `pyproject.toml` file:

```toml
[tool.projector.pip_compile]
requirements_in_dir = "deps"
requirements_out_dir = "deps/lock"
python_platforms = ["x86_64-manylinux_2_28", "aarch64-apple-darwin", "x86_64-apple-darwin"]
```

Then, run the command:

```sh
projector pip-compile
```

It will make `deps/lock/{platform}/requirements*.txt` files based on the `deps/requirements*.in` files.

### Get minimum Python version with `projector get-min-python-version`

Given the `pyproject.toml` file:

```toml
[tool.project]
requires-python = ">=3.10,<4"
```

It will output the minimum Python version:

```console
$ projector get-min-python-version
3.10
```

This is useful in CI where you want to run unit test etc. with the minimum Python version.  
For example, in GitHub Actions:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install uv
        uses: astral-sh/setup-uv@v4
      - name: Get minimum Python version
        run: |
          uv tool install python-projector
          echo "min_python_version=$(projector get-min-python-version)" >> "$GITHUB_OUTPUT"
        id: parse-python-version
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ steps.parse-python-version.outputs.min_python_version }}
      # ...
```

### Generate `__init__.py` files with `projector gen-init-py`

Generate `__init__.py` files recursively in the `src/` directory found like `projector get-src-dir`.

This is useful for mkdocs because it requires `__init__.py` in all modules.

### Run doctest with `projector run-doctest`

Run doctest with all modules in the `src/` directory found like `projector get-src-dir`.
