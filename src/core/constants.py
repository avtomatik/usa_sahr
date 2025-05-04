#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 22:00:37 2023

@author: green-machine
"""

from core.classes import Token
from core.config import ARCHIVE_NAME_UTILISED, DATA_DIR

MAP_KWARGS = {
    Token.USA_SAHR: {
        'filepath_or_buffer': DATA_DIR.joinpath(ARCHIVE_NAME_UTILISED),
        'index_col': 1,
        'usecols': range(4, 7)
    }
}
