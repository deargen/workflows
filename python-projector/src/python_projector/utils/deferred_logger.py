import logging
from collections.abc import Sequence
from typing import Any


class DeferredLogger:
    """
    A deferred logger that saves functions to log and can be used to log later.

    Useful when you want to log something before the logger is configured.

    Examples:
        >>> deferred_logger = DeferredLogger()
        >>> deferred_logger.debug("Hello, debug!")
        >>> deferred_logger.info("Hello, info!")
        >>> deferred_logger.warning("Hello, warning!")
        >>> deferred_logger.error("Hello, error!")
        >>> deferred_logger.critical("Hello, critical!")
        >>> logger = logging.getLogger(__name__)
        >>> import sys; logging.basicConfig(level=logging.WARNING, stream=sys.stdout, format="%(message)s")
        >>> deferred_logger.flush(logger)
        Hello, warning!
        Hello, error!
        Hello, critical!
    """

    def __init__(self):
        self.logs: list[tuple[str, str, Sequence[Any], dict[str, Any]]] = []

    def _log(self, func_name: str, msg: str, *args, **kwargs):
        self.logs.append((func_name, msg, args, kwargs))

    def debug(self, msg: str, *args, **kwargs):
        self._log("debug", msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        self._log("info", msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        self._log("warning", msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        self._log("error", msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs):
        self._log("critical", msg, *args, **kwargs)

    def flush(self, logger: logging.Logger):
        for func_name, msg, args, kwargs in self.logs:
            getattr(logger, func_name)(msg, *args, stacklevel=2, **kwargs)
        self.logs = []


if __name__ == "__main__":
    import doctest

    doctest.testmod()
