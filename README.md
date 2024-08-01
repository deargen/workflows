# Reusable workflows

This repository contains reusable and reference GitHub Actions workflows.

## Style checking and applying fixes

### Ruff lint and style checking

```yaml
name: Style checking

on:
  [push, pull_request]

concurrency:
  group: ${{github.workflow}}-${{github.ref}}
  cancel-in-progress: true

jobs:
  ruff-format:
    uses: deargen/workflows/.github/workflows/check-ruff.yml@master
    with:
      check-type: format
      ruff-version-file: deps/lock/x86_64-manylinux_2_28/requirements_dev.txt
  ruff-isort:
    uses: deargen/workflows/.github/workflows/check-ruff.yml@master
    with:
      check-type: isort
      ruff-version-file: deps/lock/x86_64-manylinux_2_28/requirements_dev.txt
  ruff-lint:
    uses: deargen/workflows/.github/workflows/check-ruff.yml@master
    with:
      check-type: lint 
      ruff-version-file: deps/lock/x86_64-manylinux_2_28/requirements_dev.txt
```

### Style checking for changed files only

```yaml
name: Style check on changed files

on: pull_request

concurrency:
  group: ${{github.workflow}}-${{github.ref}}
  cancel-in-progress: true

jobs:
  ruff-format-on-changes:
    uses: deargen/workflows/.github/workflows/check-ruff-only-changed.yml@master
    with:
      check-type: format
      ruff-version-file: deps/lock/x86_64-manylinux_2_28/requirements_dev.txt
  ruff-isort-on-changes:
    uses: deargen/workflows/.github/workflows/check-ruff-only-changed.yml@master
    with:
      check-type: isort
      ruff-version-file: deps/lock/x86_64-manylinux_2_28/requirements_dev.txt
  ruff-lint-on-changes:
    uses: deargen/workflows/.github/workflows/check-ruff-only-changed.yml@master
    with:
      check-type: lint
      ruff-version-file: deps/lock/x86_64-manylinux_2_28/requirements_dev.txt
```


### Apply ruff format, isort and fixes

```yaml
name: Apply ruff format, isort, and fixes

on:
  workflow_dispatch:
    inputs:
      ruff-select:
        description: 'ruff select'
        default: I,D20,D21,UP00,UP032,UP034
      ruff-ignore:
        description: 'ruff ignore'
        default: D212

jobs:
  ruff-format:
    uses: deargen/workflows/.github/workflows/apply-ruff.yml@master
    with:
      ruff-select: ${{ github.event.inputs.ruff-select }}
      ruff-ignore: ${{ github.event.inputs.ruff-ignore }}
      ruff-version-file: deps/lock/x86_64-manylinux_2_28/requirements_dev.txt
```

## Cargo clippy and fmt checking for Rust projects

```yaml
name: Style checking

on:
  [push, pull_request]

concurrency:
  group: ${{github.workflow}}-${{github.ref}}
  cancel-in-progress: true

jobs:
  check-rustfmt:
    uses: deargen/workflows/.github/workflows/check-cargo.yml@master
    with:
      check-type: fmt
      working-directory: rust
  check-clippy:
    uses: deargen/workflows/.github/workflows/check-cargo.yml@master
    with:
      check-type: clippy
      working-directory: rust
```

## Compiling requirements.txt (generate locked versions)

### Check uv pip compile

```yaml
name: Check pip compile sync

on: [push, pull_request]

concurrency:
  group: ${{github.workflow}}-${{github.ref}}
  cancel-in-progress: true

jobs:
  check-pip-compile:
    name: Check pip compile
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: deargen/workflows/actions/check-pip-compile@master
        with:
          pyproject-toml-file: pyproject.toml
          requirements-in-dir: deps
          requirements-out-dir: deps/lock
          python-platforms: x86_64-manylinux_2_28,aarch64-apple-darwin,x86_64-apple-darwin,x86_64-pc-windows-msvc
```

### Apply uv pip compile

```yaml
name: Apply pip compile (generate lockfiles)

on: workflow_dispatch

jobs:
  apply-pip-compile:
    name: Apply pip compile
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: deargen/workflows/actions/apply-pip-compile@master
        with:
          pyproject-toml-file: pyproject.toml
          requirements-in-dir: deps
          requirements-out-dir: deps/lock
          python-platforms: x86_64-manylinux_2_28,aarch64-apple-darwin,x86_64-apple-darwin,x86_64-pc-windows-msvc
```

## mkdocs build

### Generate `__init__.py` files

Without `__init__.py` files, mkdocs will not be able to generate the documentation for the package.

```yaml
name: Generate __init__.py files

on:
  workflow_dispatch:
    inputs:
      src-dir:
        description: src directory
        required: true
        default: src

jobs:
  generate-init-py:
    name: Generate __init__.py files
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: deargen/workflows/actions/gen-init-py@master
        with:
          src-dir: ${{ github.event.inputs.src-dir }}
```

### Check mkdocs build

```yaml
name: Check mkdocs build

on: pull_request

jobs:
  mkdocs:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
      - uses: deargen/workflows/actions/setup-python-and-uv@master
      - name: Check mkdocs
        uses: deargen/workflows/actions/check-mkdocs@master
        with:
          src-dir: src
          requirements-docs-file: deps/lock/x86_64-manylinux_2_28/requirements_docs.txt
```

## Testing

### Setup python, uv and run pytest and doctest

```yaml
name: Tests

on:
  - push
  - pull_request

concurrency:
  group: ${{github.workflow}}-${{github.ref}}
  cancel-in-progress: true

jobs:
  pytest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: deargen/workflows/actions/setup-python-and-uv@master
      - name: Install dependencies
        run: |
          uv venv
          source .venv/bin/activate
          uv pip install -r deps/lock/x86_64-manylinux_2_28/requirements_dev.txt
          bash scripts/install.sh
          python3 scripts/hf_download.py
      - name: Run pytest
        uses: deargen/workflows/actions/run-pytest@master

  doctest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: deargen/workflows/actions/setup-python-and-uv@master
      - name: Install dependencies
        run: |
          uv venv
          source .venv/bin/activate
          uv pip install -r deps/lock/x86_64-manylinux_2_28/requirements_dev.txt
          bash scripts/install.sh
          python3 scripts/hf_download.py
      - name: Run doctest 
        uses: deargen/workflows/actions/run-doctest@master
```

### Setup conda with cache and run pytest

```yaml
name: Tests

on:
  push:
    branches:
      - main
      - master
  pull_request:

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  pytest:
    runs-on: ubuntu-latest
    defaults:
      run:
        shell: bash -el {0} # setup-miniconda requires bash
    steps:
      - uses: actions/checkout@v4
      - name: Setup conda
        uses: deargen/workflows/actions/setup-conda-and-uv@master
      - name: Cache Conda environment
        id: cache-conda
        uses: actions/cache@v4
        env:
          cache-name: cache-conda
        with:
          path: ~/miniconda3/envs/test
          key: ${{ runner.os }}-conda-${{ env.cache-name }}-${{ hashFiles('deps/lock/x86_64-manylinux_2_28/requirements_dev.txt') }}
      - if: steps.cache-conda.outputs.cache-hit == 'true'
        run: echo 'conda cache hit!'
      - name: Install dependencies
        if: steps.cache-conda.outputs.cache-hit != 'true'
        run: |
          uv pip install -r deps/lock/x86_64-manylinux_2_28/requirements_dev.txt
          uv pip install -e .
          bash scripts/install_binaries.sh
      - name: Run pytest
        uses: deargen/workflows/actions/run-pytest@master
```

## Deploying a new version

### Commit CHANGELOG.md, create a Release and deploy MkDocs

```yaml
name: Commit CHANGELOG.md, create a Release and deploy MkDocs

on:
  workflow_dispatch:
    inputs:
      version-tag:
        description: Version tag
        required: true
        default: v0.1.0
      dry-run:
        description: Dry run
        type: boolean
        default: false

jobs:
  commit-changelog-and-release:
    uses: deargen/workflows/.github/workflows/commit-changelog-and-release.yml@master
    with:
      version-tag: ${{ github.event.inputs.version-tag }}
      dry-run: ${{ github.event.inputs.dry-run == true }}
      changelog-path: docs/CHANGELOG.md
      exclude-types: build,docs,style,other

  deploy-mkdocs:
    needs: commit-changelog-and-release
    uses: deargen/workflows/.github/workflows/deploy-mkdocs.yml@master
    with:
      requirements-file: deps/lock/x86_64-manylinux_2_28/requirements_docs.txt
      gitlab-project: deargen-ai/my-project-docs  # Remove gitlab inputs if deploying to GitHub Pages
      gitlab-branch: gl-pages
      version-tag: ${{ github.event.inputs.version-tag }}
      deploy-type: tag
    secrets:
      GITLAB_TOKEN: ${{ secrets.GITLAB_TOKEN }}
```

### Deploy MkDocs on latest commit

```yaml
name: Deploy MkDocs on latest commit

on:
  push:
    branches:
      - main
      - master

jobs:
  deploy-mkdocs:
    uses: deargen/workflows/.github/workflows/deploy-mkdocs.yml@master
    with:
      deploy-type: latest
      requirements-file: deps/lock/x86_64-manylinux_2_28/requirements_docs.txt
      gitlab-project: deargen-ai/my-project-docs  # Remove gitlab inputs if deploying to GitHub Pages
      gitlab-branch: gl-pages
    secrets:
      GITLAB_TOKEN: ${{ secrets.GITLAB_TOKEN }}
```

## Reference

This repository was inspired from [treesitter/workflows](https://github.com/treesitter/workflows).
