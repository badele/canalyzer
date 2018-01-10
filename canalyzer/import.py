# -*- coding: utf-8 -*-

import os
import yaml

import mylib
from pymarketcap import Pymarketcap

# init
coinmarketcap = Pymarketcap()
fanalyzer = open("canalyzer.yaml", "r")
yanalyzer = yaml.load(fanalyzer)

for coin in yanalyzer['analyze']:
    print ("Import %s" % coin)

    # Create folder if not exists
    currentpath = os.path.dirname(os.path.abspath(__file__))
    path = "%s/results/%s" % (currentpath, coin.upper())
    if not os.path.exists(path):
        os.makedirs(path)

    # Download last coin infos
    lastpath = "%s/last.json" % (path)
    coininfo = coinmarketcap.ticker(coin.upper())
    mylib.saveJSON(lastpath,coininfo)
