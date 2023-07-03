#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 22:00:37 2023

@author: green-machine
"""

from pathlib import Path

from core.classes import Token

ARCHIVE_NAME_UTILISED = 'dataset_usa_infcf16652007.zip'


MAP_KWARGS = {
    Token.USA_SAHR: {
        'filepath_or_buffer': Path(__file__).parent.parent.parent.joinpath('data').joinpath(ARCHIVE_NAME_UTILISED),
        'index_col': 1,
        'usecols': range(4, 7)
    }
}
