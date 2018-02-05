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

import statsmodels.formula.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std

import statsmodels.formula.api as smf
import statsmodels.tsa.api as smt
import statsmodels.api as sm

# Canalyzer
import mylib.date
import mylib.file
import mylib.text
import mylib.math
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
    periods = collections.OrderedDict(sorted(periods.items(),reverse=True))

    mindate = None
    maxdate = None
    ignoredcoins = 0

    dfallperiod = pd.DataFrame()

    fig, axr = plt.subplots(figsize=(12,9),nrows=len(periods.items()))
    fig.subplots_adjust(hspace = .5, wspace=.001)

    axline = 0
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
                    except:
                        pass

            except:
                print ("ignore plotPerfCoins #1")
                ignoredcoins += 1
                raise

        df = pd.concat(summariescoins, axis=0)
        grp = df.groupby('date')
        grp = grp.agg({'globalperf': ['mean']})

        # Plot
        globalperf = grp['globalperf']['mean']
        zeroline = globalperf*0

        # Linear
        std, middle, lower, upper = mylib.indicator.LR(globalperf)
        grp['middle'] = middle
        grp['lower'] = lower
        grp['upper'] = upper

        ax = axr[axline]
        zeroline.plot(ax=ax,color='black',style='--')
        globalperf.plot(ax=ax,label='globalperf',legend=True)

        for n in period['function']['sma']:
            SMA = mylib.indicator.SMA(globalperf,n)
            SMA.plot(ax=ax,label='SMA%s' % (n),legend=True)

        grp['middle'].plot(ax=ax,linestyle=':',label='middle',legend=True)
        grp['lower'].plot(ax=ax,linestyle=':',label='lower',legend=True)
        grp['upper'].plot(ax=ax,linestyle=':',label='upper',legend=True)

        ax.set_xlabel('')
        ax.set_ylabel('Percent (%)')
        ax.grid(True)
        ax.margins(x=0)
        title = "All coins(%s) performance %s periods / %s intervals" % (len(coins), period['rewind'],period['resample'])
        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=9,ncol=7, mode="expand", borderaxespad=0.,fontsize='x-small',title=title)

        axline += 1

    plt.savefig('/tmp/perfcoins.png')
    plt.show()



# Get markets coins information
mylib.commons.initCanalyzer()
markets = mylib.conf.getSelectedMarkets()
coins = mylib.commons.getCoins4Markets(markets)
#coins = coins[:5]

# Load all historical coins
allcoins = {}
maxrewind = getMaxRewind()
allcoins = mylib.commons.loadAllCoinsHistorical(coins,maxrewind)
plotPerfCoins(allcoins)
