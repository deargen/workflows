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
        "3.6"
    """
    range_constraints = version_range.split(",")

    min_version = Version("0.0.0")
    max_version = Version("9999.9999.9999")

    for range_constraint in range_constraints:
        range_constraint = range_constraint.strip()  # noqa: PLW2901
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
