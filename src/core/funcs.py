#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 21:34:51 2023

@author: green-machine
"""

import pandas as pd

from core.classes import Token
from core.constants import MAP_KWARGS


def read(token: Token) -> pd.DataFrame:
    """
    Read Selected Files

    Parameters
    ----------
    token : Token
        DESCRIPTION.

    Returns
    -------
    pd.DataFrame
        DESCRIPTION.

    """
    return pd.read_csv(**MAP_KWARGS.get(token))


def pull_by_series_id(df: pd.DataFrame, series_id: str) -> pd.DataFrame:
    """
    Parameters
    ----------
    df : pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series IDs
        df.iloc[:, 1]      Values
        ================== =================================
    series_id : str
    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series
        ================== =================================
    """
    assert df.shape[1] == 2
    return df[df.iloc[:, 0] == series_id].iloc[:, [1]].rename(
        columns={"value": series_id}
    )


def transform_usa_sahr_infcf(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retrieves Yearly Price Rates from ARCHIVE_NAME_UTILISED
    Returns
    -------
    pd.DataFrame
    """
    # =========================================================================
    # Retrieve First 14 Series
    # =========================================================================
    n_first_series = 14
    return (
        pd.concat(
            map(
                lambda _: df.pipe(pull_by_series_id, _).rdiv(1),
                df.iloc[:, 0].unique()[:n_first_series]
            ),
            axis=1,
            sort=True
        )
        .pct_change()
        .mul(-1)
    )
