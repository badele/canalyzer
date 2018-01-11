# -*- coding: utf-8 -*-

# Sys
import os
import sys

# Libs
import yaml
from tabulate import tabulate

# Canalyzer
import mylib

# init
fanalyzer = open("canalyzer.yaml", "r")
yanalyzer = yaml.load(fanalyzer)

coinsinfo = {
    'Symbol':[],
    'Name': [],
    'Rank': [],
    'Price(USD)': [],
    'Perf 1H': [],
    'Perf 24H': [],
    'Perf 7D': [],
}

for coin in yanalyzer['analyze']:
    # Create folder if not exists
    currentpath = os.path.dirname(os.path.abspath(__file__))
    lastpath = "%s/results/%s/last.json" % (currentpath, coin.upper())
    if os.path.exists(lastpath):
        info = mylib.loadJSON(lastpath)

        coinsinfo['Symbol'].append(info['symbol'])
        coinsinfo['Name'].append(info['name'])
        coinsinfo['Rank'].append(info['rank'])
        coinsinfo['Price(USD)'].append(info['price_usd'])
        coinsinfo['Perf 1H'].append(info['percent_change_1h'])
        coinsinfo['Perf 24H'].append(info['percent_change_24h'])
        coinsinfo['Perf 7D'].append(info['percent_change_7d'])

print (tabulate(coinsinfo,headers="keys", floatfmt=("", "",".1f",".6f",".2f",".2f",".2f")))
