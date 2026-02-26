"""Project-specific exception hierarchy."""


class DataLoadError(Exception):
    """Raised when training or ideal data cannot be loaded or validated."""


class IdealSelectionError(Exception):
    """Raised when ideal-function selection cannot be computed safely."""


class MappingError(Exception):
    """Raised when test-to-ideal mapping cannot be executed safely."""
