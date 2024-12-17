from typing import Any


class InvalidConfigError(Exception):
    pass


def get_toml_value(
    toml_dict: dict[str, Any],
    keys: list[str],
    *,
    toml_path_for_error: str = "pyproject.toml",
) -> Any:
    value = toml_dict
    for k in keys:
        if k not in value:
            key = ".".join(keys)
            raise InvalidConfigError(f"Missing key {key} in {toml_path_for_error}")
        value = value[k]
    return value
