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
import mylib.conf
import mylib.date
import mylib.file
import mylib.text
import mylib.commons
import mylib.indicator

def getPlotMaxRewind():
    # Get max rewind period for loading data
    rewinds = []

    for period in mylib.conf.yanalyzer['analyze']['function']['plotPercentPerfCoins']['period']:
        rewinds.append(pd.Timedelta(period['data']['rewind']))

    maxrewind = sorted(rewinds)[-1]

    return maxrewind

def plotPercentPerfCoins( allcoins):
    mindate = None
    maxbate = None
    ignoredcoins = 0

    dfallperiod = pd.DataFrame()

    # fig, axr = plt.subplots(figsize=(12,9),nrows=len(periods.items()))
    # fig.subplots_adjust(hspace = .5, wspace=.001)

    # Init plot
    plt.figure(figsize=(12, 14))
    ax = plt.subplot(111)

    #axline = 0
    periods = mylib.conf.yanalyzer['analyze']['function']['plotPercentPerfCoins']['period']
    for period in periods:
        pname = period['name']

        plt.clf()
        summariescoins = []

        nbcut = 0
        if 'nbcut' in period['data']:
            nbcut = period['data']['nbcut']

        rewind = '365d'
        if 'rewind' in period['data']:
            rewind = period['data']['rewind']

        resample = '1d'
        if 'resample' in period['data']:
            resample = period['data']['resample']

        for coin in allcoins:
            df = allcoins[coin]
            try:
                    try:
                        filtered = mylib.commons.filterHistorical(df, rewind)
                        resampled = mylib.commons.resampleHistorical(filtered, resample)
                        if nbcut > 0:
                            resampled = resampled[0:-nbcut]
                        summariescoins.append(resampled)

                    except (KeyboardInterrupt, SystemExit):
                        raise
                    except:
                        print  ("ERROR with %(coins)s" % locals())
                        raise

            except:
                print ("ignore plotPercentPerfCoins #1")
                ignoredcoins += 1
                raise

        df = pd.concat(summariescoins, axis=0)
        grp = df.groupby('date')
        grp = grp.agg({'globalperf': ['mean']})

        # Plot
        globalperf = grp['globalperf']['mean']
        zeroline = globalperf*0

        #ax = axr[axline]
        zeroline.plot(color='black',style='--')
        globalperf.plot(label='globalperf',legend=True)

        # Trend Line
        if 'trend_line' in period['function']:
            for options in period['function']['trend_line']:
                grp['trend_line']= mylib.indicator.trend_line(globalperf,options)

                grp['trend_line'].plot(linewidth=3, label='TrendLine',legend=True)

        # Support Line
        if 'SL' in period['function']:
            for options in period['function']['SL']:
                grp['SL'] = mylib.indicator.SL(globalperf,options)
                grp['SL'].plot(linewidth=3, label='SL',legend=True)

        # SMA
        if 'SMA' in period['function']:
            for n in period['function']['SMA']:
                grp['SMA'] = mylib.indicator.SMA(globalperf,n)
                grp['SMA'].plot(label='SMA%s' % (n),legend=True)

        # Linear
        if 'LR' in period['function']:
            for n in period['function']['LR']:
                std, middle, lower, upper = mylib.indicator.LR(globalperf,n)
                grp['middle'] = middle
                grp['lower'] = lower
                grp['upper'] = upper

                grp['middle'].plot(linestyle=':',label='middle',legend=True)
                grp['lower'].plot(linestyle=':',label='lower',legend=True)
                grp['upper'].plot(linestyle=':',label='upper',legend=True)

        if 'LR2' in period['function']:
            for n in period['function']['LR2']:
                std, middle, lower, upper = mylib.indicator.LR2(globalperf,n)
                grp['middle'] = middle
                grp['lower'] = lower
                grp['upper'] = upper

                grp['middle'].plot(linestyle=':',label='middle',legend=True)
                grp['lower'].plot(linestyle=':',label='lower',legend=True)
                grp['upper'].plot(linestyle=':',label='upper',legend=True)

        #plt.set_xlabel('')
        #plt.set_ylabel('Percent (%)')
        axu.spines["top"].set_visible(False)
        axu.spines["bottom"].set_visible(False)
        axu.spines["right"].set_visible(False)
        axu.spines["left"].set_visible(False)

        axu.get_xaxis().tick_bottom()
        axu.get_yaxis().tick_left()

        plt.ylim(globalperf.min()*1.1, globalperf.max()*1.1)
        #plt.xlim(1968, 2014)

        plt.tick_params(axis="both", which="both", bottom="off", top="off",
        labelbottom="on", left="off", right="off", labelleft="on")

        plt.grid(True)
        plt.margins(x=0)

        nbcoins = len(coins)
        rewind = period['data']['rewind']
        resample = period['data']['resample']
        title = "%(nbcoins)s coins performance / [%(pname)s / rew:%(rewind)s-res:%(resample)s]" % locals()
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=9,ncol=7, mode="expand", borderaxespad=0.,fontsize='x-small',title=title)

        destination = mylib.conf.yanalyzer['analyze']['function']['plotPercentPerfCoins']['destination']
        plt.draw()
        plt.savefig('%(destination)s/perfpercentcoins_%(pname)s.png' % locals())

def plotPricePerfCoins( allcoins):
    mindate = None
    maxbate = None
    ignoredcoins = 0

    dfallperiod = pd.DataFrame()

    # fig, axr = plt.subplots(figsize=(12,9),nrows=len(periods.items()))
    # fig.subplots_adjust(hspace = .5, wspace=.001)

    # Init plot

    #axline = 0
    periods = mylib.conf.yanalyzer['analyze']['function']['plotPercentPerfCoins']['period']
    for period in periods:
        plt.clf()
        fig = plt.figure(figsize=(16, 12))
        # axu = plt.subplot(211)
        # axb = plt.subplot(212)

        left, width = 0.05, 0.9
        rectu = [left, 0.2, width, 0.7]
        rectd = [left, 0.1, width, 0.1]

        axu = fig.add_axes(rectu)
        axb = fig.add_axes(rectd, sharex=axu)

        pname = period['name']

        summariescoins = []

        nbcut = 0
        if 'nbcut' in period['data']:
            nbcut = period['data']['nbcut']

        rewind = '365d'
        if 'rewind' in period['data']:
            rewind = period['data']['rewind']

        resample = '1d'
        if 'resample' in period['data']:
            resample = period['data']['resample']

        for coin in allcoins:
            df = allcoins[coin]
            try:
                    try:
                        filtered = mylib.commons.filterHistorical(df, rewind)
                        resampled = mylib.commons.resampleHistorical(filtered, resample)
                        if nbcut > 0:
                            resampled = resampled[0:-nbcut]
                        summariescoins.append(resampled)

                    except (KeyboardInterrupt, SystemExit):
                        raise
                    except:
                        print  ("ERROR with %(coin)s" % locals())
                        continue

            except:
                print ("ignore plotPercentPerfCoins #1")
                ignoredcoins += 1
                raise

        df = pd.concat(summariescoins, axis=0)
        df['Direction'] = np.sign(mylib.indicator.Direction(df['globalperf'],period['function']['Direction']))

        grp = df.groupby('date')
        grp = grp.agg({'globalperf': ['mean'],'Direction': ['sum']})



        # Plot
        value = grp['globalperf']['mean']
        pdirection = grp['Direction']['sum']


        #ax = axr[axline]
        value.plot(ax=axu,label='value',legend=True)
        pdirection.plot(ax=axb,label='value',legend=True)

        minvalue = value.min()
        maxvalue = value.max()

        # Trend Line
        if 'trend_line' in period['function']:
            for options in period['function']['trend_line']:
                grp['trend_line']= mylib.indicator.trend_line(value,options)
                grp['trend_line'].plot(ax=axu,linewidth=3, label='TrendLine',legend=True)
                minvalue = min(minvalue,grp['trend_line'].min())
                maxvalue = max(maxvalue,grp['trend_line'].max())

        # Support Line
        if 'SL' in period['function']:
            for options in period['function']['SL']:
                grp['SL'] = mylib.indicator.SL(value,options)
                grp['SL'].plot(ax=axu,linewidth=3, label='SL',legend=True)
                minvalue = min(minvalue,grp['SL'].min())
                maxvalue = max(maxvalue,grp['SL'].max())

        # SMA
        if 'SMA' in period['function']:
            for n in period['function']['SMA']:
                grp['SMA'] = mylib.indicator.SMA(value,n)
                grp['SMA'].plot(ax=axu,label='SMA%s' % (n),legend=True)
                minvalue = min(minvalue,grp['SMA'].min())
                maxvalue = max(maxvalue,grp['SMA'].max())

        # Linear
        if 'LR' in period['function']:
            for n in period['function']['LR']:
                std, middle, lower, upper = mylib.indicator.LR(value,n)
                grp['middle'] = middle
                grp['lower'] = lower
                grp['upper'] = upper

                grp['middle'].plot(ax=axu,linestyle=':',label='middle',legend=True)
                grp['lower'].plot(ax=axu,linewidth=3,color='r',label='lower',legend=True)
                grp['upper'].plot(ax=axu,linewidth=3,color='g',label='upper',legend=True)
                minvalue = min(minvalue,grp['lower'].min())
                maxvalue = max(maxvalue,grp['upper'].max())

        if 'LR2' in period['function']:
            for n in period['function']['LR2']:
                std, middle, lower, upper = mylib.indicator.LR2(value,n)
                grp['middle'] = middle
                grp['lower'] = lower
                grp['upper'] = upper

                grp['middle'].plot(ax=axu,linestyle=':',label='middle',legend=True)
                grp['lower'].plot(ax=axu,linewidth=3,color='r',label='lower',legend=True)
                grp['upper'].plot(ax=axu,linewidth=3,color='g',label='upper',legend=True)
                minvalue = min(minvalue,grp['lower'].min())
                maxvalue = max(maxvalue,grp['upper'].max())

        #plt.set_xlabel('')
        #plt.set_ylabel('Percent (%)')
        axu.spines["top"].set_visible(False)
        axu.spines["bottom"].set_visible(False)
        axu.spines["right"].set_visible(False)
        axu.spines["left"].set_visible(False)

        axb.spines["top"].set_visible(False)
        axb.spines["bottom"].set_visible(False)
        axb.spines["right"].set_visible(False)
        axb.spines["left"].set_visible(False)

        axu.get_xaxis().tick_bottom()
        axu.get_yaxis().tick_left()

        axb.get_xaxis().tick_bottom()
        axb.get_yaxis().tick_left()

        axu.set_ylim(minvalue,maxvalue)
        axb.set_ylim(len(coins)*-1,len(coins))
        #plt.xlim(1968, 2014)

        axu.tick_params(axis="both", which="both", bottom="off", top="off",
        labelbottom="on", left="off", right="off", labelleft="on")

        axb.tick_params(axis="both", which="both", bottom="off", top="off",
        labelbottom="on", left="off", right="off", labelleft="on")

        axu.grid(True)
        axu.margins(x=0)

        axb.grid(True)
        axb.margins(x=0)


        nbcoins = len(coins)
        rewind = period['data']['rewind']
        resample = period['data']['resample']
        title = "%(nbcoins)s coins performance / [%(pname)s / rew:%(rewind)s-res:%(resample)s]" % locals()
        axu.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=9,ncol=7, mode="expand", borderaxespad=0.,fontsize='x-small',title=title)

        #axu.minorticks_on()
        axu.grid(which='major', linestyle='-', linewidth='0.5', color='gray')
        axu.grid(which='minor', linestyle=':', linewidth='0.5', color='lightgrey')

        axb.minorticks_on()
        axb.grid(which='major', linestyle='-', linewidth='0.5', color='gray')
        axb.grid(which='minor', linestyle=':', linewidth='0.5', color='lightgrey')

        destination = mylib.conf.yanalyzer['analyze']['function']['plotPercentPerfCoins']['destination']
        plt.draw()
        plt.savefig('%(destination)s/perfpricecoins_%(pname)s.png' % locals())


# Get markets coins information
mylib.commons.initCanalyzer()
markets = mylib.conf.getSelectedMarkets()
coins = mylib.commons.getCoins4Markets(markets)
#coins = coins[:5]
#coins = ['DRPU','CHSB']

# Load all historical coins
allcoins = {}
maxrewind = getPlotMaxRewind()
allcoins = mylib.commons.loadAllCoinsHistorical(coins,maxrewind)
plotPricePerfCoins(allcoins)
