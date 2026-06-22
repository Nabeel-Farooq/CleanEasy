from __future__ import annotations

from .core import CleanEasy
from .utils import (
    convert_to_dataframe,
    get_column_types,
    setup_logger,
)
from .validators import (
    check_correlation,
    check_missing_proportion,
    check_normality,
    check_skewness,
    check_unique_values,
)

__version__ = "0.2.0"

__all__ = (
    "CleanEasy",
    "get_column_types",
    "setup_logger",
    "convert_to_dataframe",
    "check_missing_proportion",
    "check_normality",
    "check_unique_values",
    "check_skewness",
    "check_correlation",
)
