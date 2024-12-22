#!/usr/bin/env python3

from __future__ import annotations

import doctest
import importlib
import os
import sys
from os import PathLike
from pathlib import Path


def _removesuffix(s: str, suffix: str) -> str:
    """
    s.removesuffix(suffix), but for Python 3.8.
    """
    if s.endswith(suffix):
        return s[: -len(suffix)]
    return s


def run_doctest(src_dir: str | PathLike) -> tuple[int, int, int, list[str]]:
    src_dir = str(src_dir)
    if src_dir.endswith("/"):
        src_dir = src_dir[:-1]

    # find all modules in src/
    modules: list[str] = []
    for root, _dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".py"):
                # convert path to module name
                root = root.replace(f"{src_dir}/", "")
                root = root.replace("/", ".")
                modules.append(root + "." + Path(file).stem)

    # run doctest for all modules
    failed_modules = []
    num_failed = 0
    num_attempted = 0
    num_modules_with_doctest = 0
    for module_name in modules:
        module_name = _removesuffix(module_name, ".__init__")
        module = importlib.import_module(module_name)
        result = doctest.testmod(module, verbose=True)
        if result.failed > 0:
            failed_modules.append(module_name)
            print(f"🚨 doctest failed for module: {module_name}")
            print(f"🚨 {result.failed} failed out of {result.attempted} tests")
            num_failed += result.failed

        if result.attempted > 0:
            num_modules_with_doctest += 1
            num_attempted += result.attempted

    return num_modules_with_doctest, num_attempted, num_failed, failed_modules


def main():
    if len(sys.argv) != 2:
        print("Usage: python run_doctest.py <src_directory>")
        sys.exit(1)

    src_directory = sys.argv[1]

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


if __name__ == "__main__":
    main()
