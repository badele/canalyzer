# -*- coding: utf-8 -*-

# Sys
import os
import sys
import datetime

# Libs
import yaml
from tabulate import tabulate

from pymarketcap import Pymarketcap

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Canalyzer
import mylib
import mylib.date
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


# def AnalyseCoin(coin):
#     nbdays = '2d'
#     df = commons.loadCoinHistorical(coin, nbdays)
#
#     # filter two days and resample
#     #filtered = df.ix['2018-01-14 00:00:00':'2018-01-15 23:59:59']
#     r = filtered.resample(mylib.conf.yanalyzer['analyze']['period'][0]['resample'])
#
#     # Groups
#     grp = filtered.groupby([pd.Grouper(freq='1d', level='date'), 'coin'])
#     grp = grp.agg({'price_usd': ['min', 'max', 'first', 'last']})
#     grp = grp.rename({'price_usd': 'price', 'first': 'open', 'last': 'close', 'min': 'low', 'max': 'high'},
#                      axis='columns')
#
#     # Compute coin performance
#     previous = grp.shift(1)['price']['close']
#     grp['gain'] = grp['price']['close'] - previous
#     grp['perf'] = ((grp['price']['close'] / previous) - 1) * 100
#
#     return grp

def AnalyseCoin(coin, start, end, resample):
    # Compute text date
    # dayseconds = int(mylib.date.humanDurationToSecond(nbdays))
    # dt_end = datetime.datetime.now()
    # dt_end = dt_end.replace(hour=23, minute=59, second=59)
    # dt_start = dt_end - datetime.timedelta(seconds=dayseconds-1)

    df = commons.loadCoinsHistorical(coin, start, end)

    # textstart = "%02d-%02d-%02d 00:00:00" % (dt_start.year, dt_start.month, dt_start.day)
    # textend = "%02d-%02d-%02d 23:59:59" % (dt_end.year, dt_end.month, dt_end.day)

    idxdate = df.tail(1).index[0]
    (start, end ) = (mylib.date.getDateRangeFromEnd('1D', idxdate))

    # filter and resample
    filtered = df.ix[start:end]

    # # Compute perf
    # previous = filtered.shift(1)['price_usd']
    # filtered['gain'] = filtered['price_usd'] - previous
    # filtered['perf'] = ((filtered['price_usd'] / previous) - 1) * 100


    r = filtered.resample(resample)
    r = r.agg({'price_usd': ['min', 'max', 'first', 'last']})
    t = filtered.asfreq(resample,method='pad')

    previous = r['price_usd']['first'][0]
    last= r['price_usd']['last'][1]
    r['gain'] = last - previous
    r['perf'] = ((last / previous) - 1) * 100


    print (filtered)
    print (r)
    print (t)


    sys.exit()

    print(t)

    print(start)
    print(end)

    sys.exit()

    r = filtered.resample(resample)
    r = r.agg({'price_usd': ['min', 'max', 'first', 'last']})
    r = r.rename({'price_usd': 'price', 'first': 'open', 'last': 'close', 'min': 'low', 'max': 'high'},
                     axis='columns')

    print(r)

    # Compute coin performance
    previous = r.shift(1)['price']['close']
    r['gain'] = r['price']['close'] - previous
    r['perf'] = ((r['price']['close'] / previous) - 1) * 100

    return r


def perfByCoins(coinsID, start, end):

    df = commons.loadCoinsHistorical(coinsID, start, end)

    g = df.groupby(['coin']).agg({'price_usd': ['min', 'max', 'first', 'last']})
    g['gain'] = g['price_usd']['last'] - g['price_usd']['first']
    g['perf'] = ((g['price_usd']['last'] / g['price_usd']['first']) - 1) * 100

    return g

def perfForAllCoins(coinsID, start, end):

    df = perfByCoins(coinsID, start, end)

    first = df['price_usd']['first'].sum()
    last = df['price_usd']['last'].sum()


    gain = last - first
    perf = ((last / first) -1) * 100

    return ({'gain':gain, 'perf':perf})

def plotPoints(df):
    g = df.groupby([pd.Grouper(freq=resample), 'coin'])
    g = g.agg({'price_usd': ['first', 'last']})
    g['gain'] = g['price_usd']['last'] - g['price_usd']['first']
    g['direction'] = np.sign(g['gain'])

    gdir = g['direction'].groupby([pd.Grouper(freq=resample, level='date')]).sum()
    gdir[:-1].plot(legend=True)
    plt.legend(['All coins direction'])
    plt.show()

def plotPrices(df):
    g = df.groupby([pd.Grouper(freq=resample)]).agg({'price_usd': ['sum']})
    g['price_usd']['sum'][:-1].plot(legend=True)
    plt.legend(['All coins in $'])
    plt.show()

commons.initCanalyzer()
coinmarketcap = Pymarketcap()
coinsID = commons.getCoins4Markets(coinmarketcap)
coinsID = coinsID[:25]


good = 0
missing = 0
allcoins = {}

# Parameters
nbdays = mylib.conf.yanalyzer['analyze']['period'][0]['period']
resample = mylib.conf.yanalyzer['analyze']['period'][0]['resample']
drange = mylib.date.getDateRangeFromEnd(nbdays,'1D')

datacoins = commons.loadCoinsHistorical(coinsID, drange, '15min')

e = commons.extractColumn(datacoins,'price_usd')
df = pd.DataFrame(e)
df[:-1].plot(grid=True,legend=True)
plt.show()

df.to_html('/tmp/result.html')

# Points graphs
plotPoints(df)

# Prices graph
plotPrices(df)