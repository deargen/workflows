from typing import Any

from packaging.version import Version


class NotSupportedVersionRangeError(Exception):
    pass


class InvalidVersionRangeError(Exception):
    pass


def min_version_requires_python(version_range: str):
    """
    Return the minimum version of Python that satisfies the given version range.

    Examples:
        >>> min_version_requires_python(">=3.6")
        '3.6'
        >>> min_version_requires_python(">=3.6,<3.8")
        '3.6'
        >>> min_version_requires_python(">3.6,<3.8")  # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        python_projector.utils.version.NotSupportedVersionRangeError: >3.6,<3.8
        >>> min_version_requires_python("<3.6,>=3.8")  # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        python_projector.utils.version.InvalidVersionRangeError: <3.6,>=3.8
        >>> min_version_requires_python("<3.10,>=3.6")
        '3.6'
    """
    range_constraints = version_range.split(",")

    min_version = Version("0.0.0")
    max_version = Version("9999.9999.9999")

    for range_constraint in range_constraints:
        range_constraint = range_constraint.strip()
        if range_constraint.startswith(">="):
            version = Version(range_constraint[2:])
            min_version = max(version, min_version)
        elif range_constraint.startswith(">"):
            raise NotSupportedVersionRangeError(version_range)
        elif range_constraint.startswith("<="):
            version = Version(range_constraint[2:])
            max_version = min(version, max_version)
        elif range_constraint.startswith("<"):
            version = Version(range_constraint[1:])
            max_version = min(version, max_version)

    if min_version > max_version:
        raise InvalidVersionRangeError(version_range)

    return str(min_version)


def versioneer_render_chrome_ext_compat_version(pieces: dict[str, Any]) -> str:
    """
    Get versioneer version that is compatible for chrome extension.

    Note:
        - Chrome extension requires version string to be in the format of 1~4 numbers.
        - Thus, we remove git hash and dirty flag from the version string. (If dirty, add 1 to distance)
        - We also change the format of distance from +DISTANCE to .DISTANCE
    """
    if pieces["error"]:
        raise ValueError("Unable to render version")

    if pieces["closest-tag"]:
        closest_tag: str = pieces["closest-tag"]
    else:
        closest_tag = "0"

    version = closest_tag
    if pieces["distance"] or pieces["dirty"]:
        if pieces["dirty"]:
            version += f".{pieces['distance'] + 1}"
        else:
            version += f".{pieces['distance']}"

    return version
