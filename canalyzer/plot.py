# -*- coding: utf-8 -*-

# Sys
import os
import sys
import datetime
import collections

# Libs
import yaml
from tabulate import tabulate

from pymarketcap import Pymarketcap

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.tseries.frequencies import to_offset

# Canalyzer
import mylib.date
import mylib.file
import mylib.text
import mylib.commons
import mylib.indicator

def getMaxRewind():
    # Get max rewind period for loading data
    rewinds = []

    for periodname in ['analyze', 'plot']:
        for period in mylib.conf.yanalyzer[periodname]['period']:
            rewinds.append(pd.Timedelta(period['rewind']))

    maxrewind = sorted(rewinds)[-1]

    return maxrewind

def plotPerfCoins( allcoins):
    periods = mylib.conf.getPeriods('plot')

    mindate = None
    maxdate = None
    ignoredcoins = 0

    dfallperiod = pd.DataFrame()
    for key, period in periods.items():
        pname = period['name']

        summariescoins = []
        for coin in allcoins:
            df = allcoins[coin]
            try:
                    try:
                        filtered = mylib.commons.filterHistorical(df, period['rewind'])
                        resampled = mylib.commons.resampleHistorical(filtered, period['resample'])
                        summariescoins.append(resampled)

                    except (KeyboardInterrupt, SystemExit):
                        raise
                    # except:
                    #     pass

            except:
                print ("ignore plotPerfCoins #1")
                ignoredcoins += 1
                raise

        df = pd.concat(summariescoins, axis=0)

        grp = df.groupby('date')
        grp = grp.agg({'globalperf': ['mean']})

        globalperf = grp['globalperf']['mean']
        zeroline = globalperf*0

        zeroline.plot(color='black',style='--')
        ax = globalperf.plot(title="All coins performance %s periods / %s intervals" % (period['rewind'],period['resample']),label='globalperf',legend=True)
        ax.set_ylabel('Percent (%)')

        for n in period['function']['sma']:
            SMA = mylib.indicator.SMA(globalperf,n)
            SMA.plot(label='SMA%s' % (n),legend=True)

        plt.grid(True)
        plt.margins(x=0)
        plt.show()



# Get markets coins information
mylib.commons.initCanalyzer()
markets = mylib.conf.getSelectedMarkets()
coins = mylib.commons.getCoins4Markets(markets)
coins = coins[:1]

# Load all historical coins
allcoins = {}
maxrewind = getMaxRewind()
allcoins = mylib.commons.loadAllCoinsHistorical(coins,maxrewind)
plotPerfCoins(allcoins)
