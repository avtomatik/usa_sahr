#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 21:26:17 2023

@author: green-machine
"""

from enum import Enum, auto
from typing import Any

import pandas as pd
from pydantic import BaseModel, FilePath, field_validator

from .core.config import ARCHIVE_NAME_UTILISED, DATA_DIR


class DatasetType(Enum):
    """Supported dataset identifiers."""
    USA_SAHR = auto()


class DatasetConfig(BaseModel):
    """Configuration for reading a dataset with pandas."""
    filepath: FilePath
    kwargs: dict[str, Any]

    @field_validator('kwargs')
    @classmethod
    def ensure_dict(cls, v: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(v, dict):
            raise TypeError('kwargs must be a dictionary')
        return v


# ============================================================================
# Dataset registry
# ============================================================================

DATASET_REGISTRY: dict[DatasetType, DatasetConfig] = {
    DatasetType.USA_SAHR: DatasetConfig(
        filepath=DATA_DIR / ARCHIVE_NAME_UTILISED,
        kwargs={
            'index_col': 1,
            'usecols': list(range(4, 7)),
        },
    ),
}


# ============================================================================
# API
# ============================================================================

def load_dataset(dataset_type: DatasetType) -> pd.DataFrame:
    """
    Load dataset associated with a dataset type.

    Parameters
    ----------
    dataset_type : DatasetType
        Dataset identifier.

    Returns
    -------
    pd.DataFrame
        Loaded dataset.
    """
    cfg = DATASET_REGISTRY[dataset_type]
    return pd.read_csv(cfg.filepath, **cfg.kwargs)


def extract_series(df: pd.DataFrame, series_id: str) -> pd.DataFrame:
    """
    Extract a single time series by ID.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame where the first column contains series IDs,
        and the second column contains values.
    series_id : str
        Identifier of the series to extract.

    Returns
    -------
    pd.DataFrame
        One-column DataFrame with index as periods and column as values.
    """
    if df.shape[1] != 2:
        raise ValueError('Expected DataFrame with exactly two columns')

    series = df.loc[df.iloc[:, 0] == series_id, df.columns[1]]
    return series.rename(series_id).to_frame()


def compute_inflation_rates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute yearly inflation-adjusted price rates from SAHR dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Raw USA SAHR dataset.

    Returns
    -------
    pd.DataFrame
        Transformed dataset of percentage changes.
    """
    num_series_to_use = 14
    series_ids = df.iloc[:, 0].unique()[:num_series_to_use]

    series_combined = pd.concat(
        [extract_series(df, sid).rdiv(1) for sid in series_ids],
        axis=1,
        join='outer',
    )

    return series_combined.pct_change().mul(-1)


if __name__ == '__main__':
    (
        load_dataset(DatasetType.USA_SAHR)
        .pipe(compute_inflation_rates)
        .plot(grid=True, title='USA SAHR Inflation-Adjusted Rates')
    )
