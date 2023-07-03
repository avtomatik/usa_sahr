#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 21:26:17 2023

@author: green-machine
"""


from core.classes import Token
from core.funcs import read, transform_usa_sahr_infcf

if __name__ == '__main__':
    read(Token.USA_SAHR).pipe(transform_usa_sahr_infcf).plot(grid=True)
