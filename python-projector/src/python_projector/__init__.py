r"""
Initialize dotenv configuration and common directories.

The package could be installed as develop mode (`pip install -e .`) or normally (`pip install .`),
so this module tries to support both cases.

Public variables:  
- `default_log_level`: The default log level. (defaults to INFO)  
    Can be configured with the environment variable `{APP_NAME_UPPER}_LOG_LEVEL`.  
- `PROJECT_DIR`: The project directory, or None.  
    It is set to `None` if the package is NOT installed in development mode. (i.e., `pip install .`)  
    We make it None to discourage the use of this path. Only use for development.  
- `DATA_DIR`: The data directory, defaults to `{PROJECT_DIR}/data` or `~/.local/share/{APP_NAME}`.  
- `LOG_DIR`: `{DATA_DIR}/logs`.  
- `APP_CONFIG_DIR`: The directory where the `.env` file is loaded from, or None.  
- `__version__`: The version of the package.  
- `APP_NAME`: The name of the module. (alias of `__name__`) (e.g., `python_projector`)  
- `APP_NAME_UPPER`: The name of the module in uppercase. (e.g., `PYTHON_PROJECTOR`)  
- `PACKAGE_NAME`: The name of the package. (replaces `_` with `-`) (e.g., `python-projector`)  

Public functions:  
- `update_data_dirs(data_dir)`: Update the data directories after the package is loaded.  

You can configure the app with the following environment variables:  
- `{APP_NAME_UPPER}_CONFIG_DIR`: The directory to search for the `.env` file.  
- `{APP_NAME_UPPER}_DATA_DIR`: The data directory.  
- `{APP_NAME_UPPER}_LOG_LEVEL`: The default log level.  

Private variables:  
- `_env_deferred_logger`: A logger that can be used before the logging system is configured.  
    It is later used in `setup_logging()`  
"""  # fmt: skip

# ruff: noqa: PLW0603
import os
from os import PathLike
from pathlib import Path

from . import _version
from .utils.deferred_logger import DeferredLogger

__version__ = _version.get_versions()["version"]
APP_NAME = __name__
APP_NAME_UPPER = APP_NAME.upper()
PACKAGE_NAME = APP_NAME.replace("_", "-")

# ┌──────────────────────────────────────────────────────────────────────────────────┐
# │          directory definitions and environment variables / dotenv                │
# └──────────────────────────────────────────────────────────────────────────────────┘

# NOTE: The value is None if you haven't installed with `pip install -e .` (development mode).
# We make it None to discourage the use of this path. Only use for development.
PROJECT_DIR: Path | None = Path(__file__).parent.parent.parent
if PROJECT_DIR.name.startswith("python3."):
    PROJECT_DIR = None

SCRIPTS_DIR = Path(__file__).parent / "scripts"

_env_deferred_logger = DeferredLogger()


def update_data_dirs(data_dir: str | PathLike):
    """This function is exposed to allow changing the data directories after the package is loaded."""
    global DATA_DIR, LOG_DIR

    DATA_DIR = Path(data_dir)
    LOG_DIR = DATA_DIR / "logs"


data_dir = os.environ.get(f"{APP_NAME_UPPER}_DATA_DIR")
if data_dir is None or data_dir == "":
    if PROJECT_DIR is not None:
        data_dir = PROJECT_DIR / "data"
    else:
        from platformdirs import user_data_path

        _env_deferred_logger.warning(
            "⚠️ No data directory is set. "
            f"We recommend you to set the data directory with the environment variable {APP_NAME_UPPER}_DATA_DIR."
        )
        data_dir = user_data_path(__name__)
        _env_deferred_logger.warning(f"⚠️ Using {data_dir} as the data directory.")
else:
    data_dir = Path(data_dir)
    if not data_dir.absolute():
        if PROJECT_DIR is not None:
            data_dir = PROJECT_DIR / data_dir
        else:
            data_dir = Path.cwd() / data_dir
        _env_deferred_logger.warning(
            "⚠️ It is recommended to set the data directory with an absolute path.\n"
            f"Using {data_dir} as the data directory."
        )


update_data_dirs(data_dir)

default_log_level = os.environ.get(f"{APP_NAME_UPPER}_LOG_LEVEL")
if default_log_level is None:
    default_log_level = "INFO"

# ┌───────────────────────────────────────────────┐
# │          setup_logging()                      │
# └───────────────────────────────────────────────┘
import inspect
import logging
from collections.abc import Sequence
from datetime import datetime, timezone

from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme

logger = logging.getLogger(__name__)

console = Console(
    theme=Theme(
        {
            "logging.level.error": "bold red blink",
            "logging.level.critical": "red blink",
            "logging.level.warning": "yellow",
            "logging.level.success": "green",
        }
    )
)


def setup_logging(
    console_level: int | str = default_log_level,
    log_dir: str | PathLike | None = None,
    output_files: Sequence[str] = (
        "{date:%Y%m%d-%H%M%S}-{name}-{levelname}-{version}.log",
    ),
    file_levels: Sequence[int] = (logging.INFO,),
    *,
    log_init_messages: bool = True,
    console_formatter: logging.Formatter | None = None,
    file_formatter: logging.Formatter | None = None,
):
    r"""
    Setup logging with RichHandler and FileHandler.

    You should call this function at the beginning of your script.

    Args:
        console_level: Logging level for console. Defaults to INFO or env var {APP_NAME_UPPER}_LOG_LEVEL.
        log_dir: Directory to save log files. If None, only console logging is enabled. Usually set to LOG_DIR.
        output_files: List of output file paths, relative to log_dir. Only applies if log_dir is not None.
        file_levels: List of logging levels for each output file. Only applies if log_dir is not None.
        log_init_messages: Whether to log the initialisation messages.
    """
    assert len(output_files) == len(
        file_levels
    ), "output_files and file_levels must have the same length"

    if log_dir is None:
        output_files = []
        file_levels = []
    else:
        log_dir = Path(log_dir)

    # NOTE: Initialise with NOTSET level and null device, and add stream handler separately.
    # This way, the root logging level is NOTSET (log all), and we can customise each handler's behaviour.
    # If we set the level during the initialisation, it will affect to ALL streams,
    # so the file stream cannot be more verbose (lower level) than the console stream.
    logging.basicConfig(
        format="",
        level=logging.NOTSET,
        stream=open(os.devnull, "w"),  # noqa: SIM115
    )

    # If you want to suppress logs from other modules, set their level to WARNING or higher
    # logging.getLogger('slowfast.utils.checkpoint').setLevel(logging.WARNING)

    console_handler = RichHandler(
        level=console_level,
        show_time=True,
        show_level=True,
        show_path=True,
        rich_tracebacks=True,
        tracebacks_show_locals=True,
        console=console,
    )

    if console_formatter is None:
        console_format = logging.Formatter(
            fmt="%(name)s - %(message)s",
            datefmt="%H:%M:%S",
        )
    else:
        console_format = console_formatter
    console_handler.setFormatter(console_format)

    if file_formatter is None:
        f_format = logging.Formatter(
            fmt="%(asctime)s - %(name)s: %(lineno)4d - %(levelname)s - %(message)s",
            datefmt="%y/%m/%d %H:%M:%S",
        )
    else:
        f_format = file_formatter

    function_caller_module = inspect.getmodule(inspect.stack()[1][0])
    if function_caller_module is None:
        name_or_path = "unknown"
    elif function_caller_module.__name__ == "__main__":
        if function_caller_module.__file__ is None:
            name_or_path = function_caller_module.__name__
        elif PROJECT_DIR is not None:
            # Called from files in the project directory.
            # Instead of using the __name__ == "__main__", infer the module name from the file path.
            name_or_path = function_caller_module.__file__.replace(
                str(PROJECT_DIR) + "/", ""
            ).replace("/", ".")
            # Remove .py extension
            name_or_path = Path(name_or_path).with_suffix("")
        else:
            # Called from somewhere outside the project directory.
            # Use the script name, like "script.py"
            name_or_path = Path(function_caller_module.__file__).name
    else:
        name_or_path = function_caller_module.__name__

    log_path_map = {
        "name": name_or_path,
        "version": __version__,
        "date": datetime.now(timezone.utc),
    }

    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)

    if log_init_messages:
        logger.info(f"{PACKAGE_NAME} {__version__}")
        _env_deferred_logger.flush(logger)

    if log_dir is not None:
        log_paths: list[Path] = []
        for output_file, file_level in zip(output_files, file_levels, strict=True):
            log_path_map["levelname"] = logging._levelToName[file_level]
            log_path = log_dir / output_file.format_map(log_path_map)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            log_paths.append(log_path)

            f_handler = logging.FileHandler(log_path)
            f_handler.setLevel(file_level)
            f_handler.setFormatter(f_format)

            # Add handlers to the logger
            root_logger.addHandler(f_handler)

        if log_init_messages:
            for log_path in log_paths:
                logger.info(f"Logging to {log_path}")
