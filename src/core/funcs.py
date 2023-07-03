#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 21:34:51 2023

@author: green-machine
"""


import pandas as pd
from core.classes import Token
from core.constants import MAP_KWARGS
from pandas import DataFrame


def read(token: Token) -> DataFrame:
    """
    Read Selected Files

    Parameters
    ----------
    token : Token
        DESCRIPTION.

    Returns
    -------
    DataFrame
        DESCRIPTION.

    """
    return pd.read_csv(**MAP_KWARGS.get(token))


def pull_by_series_id(df: DataFrame, series_id: str) -> DataFrame:
    """
    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series IDs
        df.iloc[:, 1]      Values
        ================== =================================
    series_id : str
    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series
        ================== =================================
    """
    assert df.shape[1] == 2
    return df[df.iloc[:, 0] == series_id].iloc[:, [1]].rename(
        columns={"value": series_id}
    )


def transform_usa_sahr_infcf(df: DataFrame) -> DataFrame:
    """
    Retrieves Yearly Price Rates from ARCHIVE_NAME_UTILISED
    Returns
    -------
    DataFrame
    """
    # =========================================================================
    # Retrieve First 14 Series
    # =========================================================================
    return pd.concat(
        map(
            lambda _: df.pipe(pull_by_series_id, _).rdiv(1),
            df.iloc[:, 0].unique()[:14]
        ),
        axis=1,
        sort=True
    ).pct_change().mul(-1)
