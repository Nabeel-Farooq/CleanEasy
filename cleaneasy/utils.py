from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

import numpy as np
import pandas as pd


DataInput = Union[
    pd.DataFrame,
    np.ndarray,
    List[Any],
    Dict[str, Any],
    str,
    Path,
]


def get_column_types(df: pd.DataFrame) -> Dict[str, str]:
    """
    Return a mapping of column names to their pandas data types.
    """
    return df.dtypes.astype(str).to_dict()


def setup_logger(
    log_level: str = "INFO",
    logger_name: str = "CleanEasy",
) -> logging.Logger:
    """
    Create or retrieve a configured logger.

    Parameters
    ----------
    log_level : str
        Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    logger_name : str
        Name of the logger.

    Returns
    -------
    logging.Logger
    """
    logger = logging.getLogger(logger_name)

    try:
        level = getattr(logging, log_level.upper())
    except AttributeError as exc:
        raise ValueError(
            f"Invalid log level '{log_level}'."
        ) from exc

    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
            )
        )
        logger.addHandler(handler)

    logger.propagate = False

    return logger


def convert_to_dataframe(
    data: DataInput,
    columns: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Convert supported data structures into a pandas DataFrame.

    Supported inputs:
    - pandas.DataFrame
    - numpy.ndarray
    - list
    - dict
    - CSV file path (str or Path)

    Parameters
    ----------
    data : DataInput
        Input data.
    columns : list[str] | None
        Optional column names.

    Returns
    -------
    pd.DataFrame

    Raises
    ------
    ValueError
        If input data is invalid or unsupported.
    """

    if isinstance(data, pd.DataFrame):
        return data.copy(deep=True)

    if isinstance(data, np.ndarray):
        if data.ndim == 1:
            data = data.reshape(-1, 1)

        if columns is None:
            columns = [f"col_{i}" for i in range(data.shape[1])]

        if len(columns) != data.shape[1]:
            raise ValueError(
                f"Expected {data.shape[1]} column names, "
                f"received {len(columns)}."
            )

        return pd.DataFrame(data, columns=columns)

    if isinstance(data, list):
        if not data:
            raise ValueError("Cannot create DataFrame from an empty list.")

        if all(isinstance(item, dict) for item in data):
            return pd.DataFrame(data)

        first_item = data[0]

        if isinstance(first_item, (list, tuple)):
            expected_cols = len(first_item)

            if columns is None:
                columns = [f"col_{i}" for i in range(expected_cols)]

            if len(columns) != expected_cols:
                raise ValueError(
                    f"Expected {expected_cols} column names, "
                    f"received {len(columns)}."
                )

            return pd.DataFrame(data, columns=columns)

        if columns is None:
            columns = ["col_0"]

        if len(columns) != 1:
            raise ValueError(
                "One-dimensional lists require exactly one column name."
            )

        return pd.DataFrame(data, columns=columns)

    if isinstance(data, dict):
        return pd.DataFrame(data)

    if isinstance(data, (str, Path)):
        file_path = Path(data)

        if not file_path.exists():
            raise ValueError(
                f"File does not exist: {file_path}"
            )

        try:
            return pd.read_csv(file_path)
        except Exception as exc:
            raise ValueError(
                f"Failed to read CSV file '{file_path}': {exc}"
            ) from exc

    raise TypeError(
        "Unsupported data type. Expected DataFrame, ndarray, "
        "list, dict, CSV path string, or Path object."
    )
