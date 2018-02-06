# -*- coding: utf-8 -*-

import os
import yaml
import collections

import pandas as pd
from pymarketcap import Pymarketcap


# init
fanalyzer = open("canalyzer.yaml", "r")
yanalyzer = yaml.load(fanalyzer)
coinmarketcap = None

# For fast starting the canalyzer app
# Only use instancing if needed
def initCoinMarketCap():
    global coinmarketcap

    if not coinmarketcap:
        coinmarketcap = Pymarketcap()

    return coinmarketcap

def getSelectedMarkets():
    return yanalyzer['select']['market']

# def getPeriods(section):
#     periods = collections.OrderedDict()
#     for period in yanalyzer[section]['period']:
#         periods[pd.Timedelta(period['resample'])] = period
#
#     return collections.OrderedDict(sorted(periods.items()))
