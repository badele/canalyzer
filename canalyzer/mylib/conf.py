# -*- coding: utf-8 -*-

import yaml
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