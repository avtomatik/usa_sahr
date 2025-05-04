#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  4 17:56:55 2025

@author: alexandermikhailov
"""

from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

DATA_DIR = BASE_DIR.joinpath('data')

ARCHIVE_NAME_UTILISED = 'dataset_usa_infcf16652007.zip'
