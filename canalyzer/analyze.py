# -*- coding: utf-8 -*-

# Sys
import os
import sys

# Libs
import yaml
from tabulate import tabulate

import numpy as np
import pandas as pd

# Canalyzer
import mylib
from mylib import commons

# def analyseAllCoinsPerf(coins,nbdays=1):
#     oneday = int(mylib.date.humanDurationToSecond("1d"))
#     end = int(mylib.date.getNow()) - oneday
#     dend = datetime.datetime.fromtimestamp(int(end))
#     dstart = dend - datetime.timedelta(days=nbdays)
#
#
#     tstart = datetime.datetime(dstart.year, dstart.month, dstart.day)
#     datetext = "%02d-%02d-%02d" % (tstart.year, tstart.month, tstart.day)
#     startfilename = "daily_%s.json" % datetext
#
#     tend = datetime.datetime(dend.year, dend.month, dend.day)
#     datetext = "%02d-%02d-%02d" % (tend.year, tend.month, tend.day)
#     endfilename = "daily_%s.json" % datetext
#
#     sumstart = []
#     sumend = []
#     for coin in coins:
#         try:
#             coinpath = "%s/%s" % (coinspath, coin.upper())
#
#             # Search we have two history
#             startfullname = "%s/%s" % (coinpath, startfilename)
#             endfullname = "%s/%s" % (coinpath, endfilename)
#             if not os.path.exists(startfullname) or not os.path.exists(endfullname):
#                 continue
#
#             jstart = mylib.file.loadJSON(startfullname)
#             jend = mylib.file.loadJSON(endfullname)
#
#
#             sumstart.append(jstart['close'])
#             sumend.append(jend['close'])
#
#         except (KeyboardInterrupt, SystemExit):
#             raise
#
#
#     nstart = np.sum(np.array(sumstart))
#     nend = np.sum(np.array(sumend))
#     ratio = ((nend/nstart)-1)*100
#
#     marketcount = len(mylib.conf.yanalyzer['select']['market'])
#     coincount = 0
#     for market in mylib.conf.yanalyzer['select']['market']:
#         try:
#             exchanges = coinmarketcap.exchange(market)
#             coincount += len(exchanges)
#         except:
#             pass
#
#     print ("%.02f %% trend for %s market(s) and %s coin(s)" % (ratio, marketcount, coincount))




# coinsinfo = {
#     'Symbol':[],
#     'Name': [],
#     'Rank': [],
#     'Price(USD)': [],
#     'Perf 1H': [],
#     'Perf 24H': [],
#     'Perf 7D': [],
# }
#
# for coin in yanalyzer['analyze']:
#     # Create folder if not exists
#     currentpath = os.path.dirname(os.path.abspath(__file__))
#     lastpath = "%s/results/%s/last.json" % (currentpath, coin.upper())
#     if os.path.exists(lastpath):
#         info = mylib.loadJSON(lastpath)
#
#         coinsinfo['Symbol'].append(info['symbol'])
#         coinsinfo['Name'].append(info['name'])
#         coinsinfo['Rank'].append(info['rank'])
#         coinsinfo['Price(USD)'].append(info['price_usd'])
#         coinsinfo['Perf 1H'].append(info['percent_change_1h'])
#         coinsinfo['Perf 24H'].append(info['percent_change_24h'])
#         coinsinfo['Perf 7D'].append(info['percent_change_7d'])
#
# print (tabulate(coinsinfo,headers="keys", floatfmt=("", "",".1f",".6f",".2f",".2f",".2f")))

commons.initCanalyzer()

df = commons.loadCoinHistorical("BCN",mylib.conf.yanalyzer['analyze']['period'][0]['period'])
r = df.resample('10min')
result = r.agg(['min','mean','max'])


print (result['price_usd'])
