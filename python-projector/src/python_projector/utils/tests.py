import doctest
import importlib
import os
from os import PathLike
from pathlib import Path


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
        module_name = module_name.removesuffix(".__init__")
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
