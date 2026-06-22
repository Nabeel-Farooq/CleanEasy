from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Union

import numpy as np
import pandas as pd
from scipy import stats


ColumnSelector = Optional[Union[str, List[str]]]


def _resolve_columns(
    df: pd.DataFrame,
    columns: ColumnSelector = None,
    *,
    numeric_only: bool = False,
) -> List[str]:
    """
    Resolve and validate column selection.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    columns : str | list[str] | None
        Columns to select. If None, all columns (or numeric columns when
        numeric_only=True) are selected.
    numeric_only : bool
        Restrict selection to numeric columns.

    Returns
    -------
    list[str]
        Valid column names present in the dataframe.
    """
    if columns is None:
        selected: Iterable[str] = (
            df.select_dtypes(include=[np.number]).columns
            if numeric_only
            else df.columns
        )
    elif isinstance(columns, str):
        selected = [columns]
    else:
        selected = columns

    valid_columns = [col for col in selected if col in df.columns]

    if numeric_only:
        numeric_columns = set(df.select_dtypes(include=[np.number]).columns)
        valid_columns = [col for col in valid_columns if col in numeric_columns]

    return valid_columns


def check_missing_proportion(df: pd.DataFrame) -> Dict[str, float]:
    """
    Return the proportion of missing values for each column.
    """
    return df.isna().mean().to_dict()


def check_normality(
    df: pd.DataFrame,
    columns: ColumnSelector = None,
) -> Dict[str, float]:
    """
    Perform the Shapiro-Wilk normality test on numeric columns.

    Returns
    -------
    dict[str, float]
        Mapping of column name to p-value.
    """
    results: Dict[str, float] = {}

    for col in _resolve_columns(df, columns, numeric_only=True):
        values = df[col].dropna()

        # Shapiro requires at least 3 observations
        if len(values) < 3:
            results[col] = np.nan
            continue

        try:
            _, p_value = stats.shapiro(values)
            results[col] = float(p_value)
        except Exception:
            results[col] = np.nan

    return results


def check_unique_values(
    df: pd.DataFrame,
    columns: ColumnSelector = None,
    *,
    dropna: bool = True,
) -> Dict[str, int]:
    """
    Return the number of unique values per column.

    Parameters
    ----------
    dropna : bool
        Whether NaN values should be excluded from the count.
    """
    return {
        col: int(df[col].nunique(dropna=dropna))
        for col in _resolve_columns(df, columns)
    }


def check_skewness(
    df: pd.DataFrame,
    columns: ColumnSelector = None,
) -> Dict[str, float]:
    """
    Compute skewness for numeric columns.
    """
    return {
        col: float(df[col].skew())
        for col in _resolve_columns(df, columns, numeric_only=True)
    }


def check_correlation(
    df: pd.DataFrame,
    columns: ColumnSelector = None,
    method: str = "pearson",
) -> pd.DataFrame:
    """
    Compute a correlation matrix for numeric columns.

    Supported methods:
    - pearson
    - spearman
    - kendall
    """
    valid_methods = {"pearson", "spearman", "kendall"}

    if method not in valid_methods:
        raise ValueError(
            f"Invalid correlation method '{method}'. "
            f"Expected one of {sorted(valid_methods)}."
        )

    selected_columns = _resolve_columns(
        df,
        columns,
        numeric_only=True,
    )

    if not selected_columns:
        return pd.DataFrame()

    return df[selected_columns].corr(method=method)
