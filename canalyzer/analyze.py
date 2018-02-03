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
#     df = mylib.commons.loadCoinHistorical(coin, nbdays)
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


# def perfByCoins(coinsID, start, end):
#
#     df = mylib.commons.loadCoinsHistorical(coinsID, start, end)
#
#     g = df.groupby(['coin']).agg({'price_usd': ['min', 'max', 'first', 'last']})
#     g['gain'] = g['price_usd']['last'] - g['price_usd']['first']
#     g['perf'] = ((g['price_usd']['last'] / g['price_usd']['first']) - 1) * 100
#
#     return g
#
# def plotPoints(df):
#     g = df.groupby([pd.Grouper(freq=resample), 'coin'])
#     g = g.agg({'price_usd': ['first', 'last']})
#     g['gain'] = g['price_usd']['last'] - g['price_usd']['first']
#     g['direction'] = np.sign(g['gain'])
#
#     gdir = g['direction'].groupby([pd.Grouper(freq=resample, level='date')]).sum()
#     gdir[:-1].plot(legend=True)
#     plt.legend(['All coins direction'])
#     plt.show()
#
# def plotPrices(df):
#     g = df.groupby([pd.Grouper(freq=resample)]).agg({'price_usd': ['sum']})
#     g['price_usd']['sum'][:-1].plot(legend=True)
#     plt.legend(['All coins in $'])
#     plt.show()

# def analyzeDataPerf(data, compare):
#     data['previous'] = data['price_usd'].shift(compare)
#     data['gain'] = data['price_usd'] - data['previous']
#     data['perf'] = ((data['price_usd'] / data['previous']) - 1) * 100
#     data['perf_direction'] = np.sign(data['perf'])
#
#     data.to_csv('/tmp/result.csv')
#     data.to_html('/tmp/result.html')
#
#     return data

# def getPerfCoinsDirection():
#     # Parameters
#     nbdays = mylib.conf.yanalyzer['analyze']['period'][0]['period']
#     resample = mylib.conf.yanalyzer['analyze']['period'][0]['resample']
#     compare = mylib.conf.yanalyzer['analyze']['period'][0]['compare']
#
#     # Compute periods comparation offset
#     now = mylib.date.getNow()
#     coffset = pd.Timedelta('1D') / np.timedelta64(1, 's')
#     dt_now = datetime.datetime.fromtimestamp(int(now))
#     dt_end = datetime.datetime.fromtimestamp(int(now + coffset))
#     periods = len(pd.date_range(start=dt_now, end=dt_end, freq=resample, closed='left'))
#
#     # Plot perf
#     drange = mylib.date.getDateRangeFromEnd(nbdays, '1D')
#     datascoins = dict()
#     for coin in coins:
#         data = mylib.commons.loadCoinHistorical(coin, drange, freq=resample)
#         if len(data) > 0:
#             data = analyzeDataPerf(data, periods)
#             datascoins[coin] = data
#
#
#     df = pd.DataFrame(mylib.commons.extractColumn(datascoins, 'perf'))
#     return df

# def column_color(col):
#     if 'perf_' in col.name:
#         is_neg = col < 0
#         return ['background-color: red' if v else 'background-color: green' for v in is_neg]
#
#     if 'gain_' in col.name:
#         is_neg = col < 0
#         return ['color: red' if v else 'color: green' for v in is_neg]
#
#     return [''] * len(col)

# def negative_background(val):
#     bg = ''
#     if type(val) == float and val < 0:
#         bg = 'background-color: red'
#
#     return bg


def getMaxRewind():
    # Get max rewind period for loading data
    rewinds = []

    for periodname in ['analyze', 'plot']:
        for period in mylib.conf.yanalyzer[periodname]['period']:
            rewinds.append(pd.Timedelta(period['rewind']))

    maxrewind = sorted(rewinds)[-1]

    return maxrewind

# def summaryCoins(coins):
#
#     # Sort period column
#     periodcolumns = collections.OrderedDict()
#     for period in mylib.conf.yanalyzer['analyze']['period']:
#         periodcolumns[pd.Timedelta(period['resample'])] = period['name']
#
#     datas = mylib.commons.loadAllCoinsHistorical3(coins, maxrewind)
#
#     # Resample all coins historical datas
#     periods = {}
#     for period in mylib.conf.yanalyzer['analyze']['period']:
#         print ("analyze %s with %s resample period" % (period['name'], period['resample']))
#         periods[period['name']] = mylib.commons.resampleAllCoinsHistorical(datas, period['rewind'], period['resample'])
#
#     # Compute columns values
#     minperiodidx = list(periodcolumns)[0]
#     minperiodname = periodcolumns[pd.Timedelta(minperiodidx)]
#     column = {'firstdate':{}, 'lastdate': {}, 'nbdays': {}}
#     for period in periods:
#         columnperf = "perf_%s" % period
#         column[columnperf] = {}
#         if minperiodname == period:
#             columnprice = "lastprice_%s" % minperiodname
#             column[columnprice] = {}
#
#         for coin in periods[period]:
#             if len(periods[period][coin]) <= 0:
#                 continue
#
#             if minperiodname == period:
#                 column[columnprice][coin] = periods[period][coin]['last'][-1]
#
#             # Compute coins performance
#             column[columnperf][coin] = {}
#
#             # Search the first date for coin
#             if coin not in column['firstdate']:
#                 column['firstdate'][coin] = periods[period][coin].index[0]
#             column['firstdate'][coin] = min(periods[period][coin].index[0],column['firstdate'][coin])
#
#             # Search the last date for coin
#             if coin not in column['lastdate']:
#                 column['lastdate'][coin] = periods[period][coin].index[-1]
#             column['lastdate'][coin] = max(periods[period][coin].index[-1],column['lastdate'][coin])
#
#             column['nbdays'][coin] = column['lastdate'][coin] - column['firstdate'][coin]
#             column[columnperf][coin] = periods[period][coin]['perf'][-1]
#
#     columnname = []
#     columnname.append("lastprice_%s" % minperiodname)
#     for period in periodcolumns:
#         columnname.append('perf_%s' % periodcolumns[period])
#     # columnname.append('firstdate')
#     # columnname.append('lastdate')
#     columnname.append('nbdays')
#
#     df = pd.DataFrame(column,columns=columnname)
#     return df

def globalPerfCoins(markets, allcoins):
    # Simulation money value
    simulatemoney = mylib.conf.yanalyzer['analyze']['simulate']['money']

    periods = mylib.conf.getPeriods('analyze')

    summariescoins = []
    mindate = None
    maxdate = None
    ignoredcoins = 0
    for coin in allcoins:
        df = allcoins[coin]

        try:
            firstdate = df.index[0]
            lastdate = df.index[-1]
            if not mindate:
                    mindate = firstdate
            if not maxdate:
                    maxdate = lastdate

            mindate = min(firstdate,mindate)
            maxdate = max(lastdate,maxdate)

            dfallperiod = pd.DataFrame()
            for key, period in periods.items():
                pname = period['name']

                try:
                    dfperiod = mylib.commons.SumarizeHistorical(df, period['rewind'], period['resample'])

                    dfperiod = dfperiod.rename({
                        'firstprice': 'firstprice_%s' % pname,
                        'lastprice': 'lastprice_%s' % pname,
                        'gain': 'gain_%s' % pname,
                        'perf': 'perf_%s' % pname,
                        'firstdate': 'firstdate_%s' % pname,
                        'lastdate': 'lastdate_%s' % pname,
                        'missingafter': 'missingafter_%s' % pname,
                        'missingbefore': 'missingbefore_%s' % pname},
                        axis='columns'
                    )
                    dfperiod['simulategain_%s' % pname] = simulatemoney * (dfperiod['perf_%s' % pname]/100)

                    if (len(dfallperiod)==0):
                        dfallperiod = dfperiod
                    else:
                        dfallperiod = pd.merge(dfperiod, dfallperiod, on='coin')

                except (KeyboardInterrupt, SystemExit):
                    raise
                # except:
                #     pass

        except:
            ignoredcoins +=1
            raise

        summariescoins.append(dfallperiod)

    try:
        df = pd.concat(summariescoins, axis=0)

        count = len(df)
        if count==0:
            text = mylib.text.getTitleText("No more data for analyzing")
            text += mylib.text.getLineText()
            return text

        df.set_index('coin', inplace=True)


        lines1 = []
        lines1.append([["Number markets", len(markets)]])
        lines1.append([["Number coins for all markets (ignored)", "%s ()%s)" % (len(coins),ignoredcoins)]])
        lines1.append([["Simulate performance Total/earch coin", "%s$/%s$" % (simulatemoney,simulatemoney*len(coins))]])
        lines1.append([["Min date", mindate],["Max date", maxdate]])

        lines2 = []
        for key, period in periods.items():
            pname = period['name']

            if 'simulategain_%s' % pname in df:
                perf = df['simulategain_%s' % pname].sum() / (count*simulatemoney) * 100
                gain = df['simulategain_%s' % pname].sum()
                lines2.append([['Gain %s' % pname, gain],['Perf %s' % pname, "%.2f" % perf]])

        #missingbefore = df['missingbefore_1D'].max()
        #missingafter = df['missingafter_1H'].min()

        #lines2.append([["Missingbefore", missingbefore],["Missingafter", missingafter]])

        # Show Result
        text = mylib.text.getTitleText("Main coins informations")
        text += mylib.text.getLineText()
        text += mylib.text.convertArray2ColumnText(lines1)
        text += mylib.text.getLineTitleText("Simulation coins performance")
        text += mylib.text.convertArray2ColumnText(lines2)
        text += mylib.text.getLineText()

    except (KeyboardInterrupt, SystemExit):
        raise
#    except:
#        pass
#    s = df.style.apply(column_color)
#    mylib.file.saveto('/tmp/result.html', str(s.render()).encode())

    return text

def plotPerfCoins( allcoins):
    # Simulation money value
    periods = mylib.conf.getPeriods('plot')

    summariescoins = []
    mindate = None
    maxdate = None
    ignoredcoins = 0

    dfallperiod = pd.DataFrame()
    for key, period in periods.items():
        pname = period['name']

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

        grp = df.groupby(['date'])
        grp = grp.agg({'simulategain': ['sum']})

        grp['zeroline'] = 0
        simulatemoney = mylib.conf.yanalyzer['analyze']['simulate']['money']
        grp['simulategain']['sum'].plot(title="All coins performance with %s$ on %s coins" % (simulatemoney*len(coins),len(coins)),label='simulategain',legend=True)
        grp['zeroline'].plot(color='black',grid=True,style='--')
        plt.margins(x=0)
        plt.show()
        sys.exit()

    try:
        df = pd.concat(summariescoins, axis=0)

        count = len(df)
        if count==0:
            text = mylib.text.getTitleText("No more data for analyzing")
            text += mylib.text.getLineText()
            return text

        df.set_index('coin', inplace=True)


        lines1 = []
        lines1.append([["Number markets", len(markets)]])
        lines1.append([["Number coins for all markets (ignored)", "%s ()%s)" % (len(coins),ignoredcoins)]])
        lines1.append([["Simulate performance Total/earch coin", "%s$/%s$" % (simulatemoney,simulatemoney*len(coins))]])
        lines1.append([["Min date", mindate],["Max date", maxdate]])

        lines2 = []
        for key, period in periods.items():
            pname = period['name']

            if 'simulategain_%s' % pname in df:
                perf = df['simulategain_%s' % pname].sum() / (count*simulatemoney) * 100
                gain = df['simulategain_%s' % pname].sum()
                lines2.append([['Gain %s' % pname, gain],['Perf %s' % pname, "%.2f" % perf]])

        #missingbefore = df['missingbefore_1D'].max()
        #missingafter = df['missingafter_1H'].min()

        #lines2.append([["Missingbefore", missingbefore],["Missingafter", missingafter]])

        # Show Result
        text = mylib.text.getTitleText("Main coins informations")
        text += mylib.text.getLineText()
        text += mylib.text.convertArray2ColumnText(lines1)
        text += mylib.text.getLineTitleText("Simulation coins performance")
        text += mylib.text.convertArray2ColumnText(lines2)
        text += mylib.text.getLineText()

    except (KeyboardInterrupt, SystemExit):
        raise
#    except:
#        pass
#    s = df.style.apply(column_color)
#    mylib.file.saveto('/tmp/result.html', str(s.render()).encode())

    return text

datas = {}
mylib.commons.initCanalyzer()
markets = mylib.conf.getSelectedMarkets()
coins = mylib.commons.getCoins4Markets(markets)
coins = coins[:10]

good = 0
missing = 0
allcoins = {}

# Load all historical coins
maxrewind = getMaxRewind()
allcoins = mylib.commons.loadAllCoinsHistorical(coins,maxrewind)

plotPerfCoins(allcoins)

text = globalPerfCoins(markets, allcoins)
print(text)
#summaryPerfCoins(coins)
sys.exit()

# # Summary Coins
# df = summaryCoins(coins)
# print (df.to_dict())
# s = df.style.applymap(color_negative_red)
# mylib.file.saveto('/tmp/result.html',str(s.render()).encode())
# sys.exit()
#
# df = getcoinsPerf24h2()
# print ("Last datas: %s" % df.index[-1])
# df.tail(1)
# print (df)
# sys.exit()

# df[:-1].plot(subplots=True, grid=True, legend=True, kind='area', stacked=False)
# plt.title('all coins perf for %s coins' % len(coins))
# #plt.legend(['perf in %'])
# plt.show()
#
# # Points graphs
# plotPoints(df)
#
# # Prices graph
# plotPrices(df)
