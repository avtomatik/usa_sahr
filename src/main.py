#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 21:26:17 2023

@author: green-machine
"""

from enum import Enum, auto
from pathlib import Path
from typing import Any

import pandas as pd
import tomllib
from pydantic import BaseModel, FilePath, field_validator

from .core.config import BASE_DIR


class DatasetType(Enum):
    """Supported dataset identifiers."""
    USA_SAHR = auto()
    # Add more enums as needed


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


def load_registry(config_path: Path) -> dict[DatasetType, DatasetConfig]:
    """Load dataset registry from a TOML configuration file."""
    with config_path.open('rb') as f:
        raw_config = tomllib.load(f)

    registry: dict[DatasetType, DatasetConfig] = {}
    for dataset_name, config in raw_config.items():
        try:
            dataset_type = DatasetType[dataset_name]
        except KeyError as e:
            raise ValueError(f'Unknown dataset type: {dataset_name}') from e

        registry[dataset_type] = DatasetConfig(**config)

    return registry


# ============================================================================
# API
# ============================================================================

def load_dataset(
    dataset_type: DatasetType,
    registry: dict[DatasetType, DatasetConfig]
) -> pd.DataFrame:
    """
    Load dataset associated with a dataset type.

    Parameters
    ----------
    dataset_type : DatasetType
        Dataset identifier.
    registry : dict
        Dataset registry loaded from TOML.

    Returns
    -------
    pd.DataFrame
        Loaded dataset.
    """
    cfg = registry[dataset_type]
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
    config_path = BASE_DIR / 'datasets.toml'
    registry = load_registry(config_path)

    (
        load_dataset(DatasetType.USA_SAHR, registry)
        .pipe(compute_inflation_rates)
        .plot(grid=True, title='USA SAHR Inflation-Adjusted Rates')
    )
