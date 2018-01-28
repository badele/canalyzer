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

def AnalyseCoin(coin, start, end, resample):
    # Compute text date
    # dayseconds = int(mylib.date.humanDurationToSecond(nbdays))
    # dt_end = datetime.datetime.now()
    # dt_end = dt_end.replace(hour=23, minute=59, second=59)
    # dt_start = dt_end - datetime.timedelta(seconds=dayseconds-1)

    df = mylib.commons.loadCoinsHistorical(coin, start, end)

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

    df = mylib.commons.loadCoinsHistorical(coinsID, start, end)

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

def plotPerfCoins():
    # Parameters
    nbdays = mylib.conf.yanalyzer['analyze']['period'][0]['period']
    resample = mylib.conf.yanalyzer['analyze']['period'][0]['resample']
    compare = mylib.conf.yanalyzer['analyze']['period'][0]['compare']

    # Compute periods comparation offset
    now = mylib.date.getNow()
    coffset = pd.Timedelta('1D') / np.timedelta64(1, 's')
    dt_now = datetime.datetime.fromtimestamp(int(now))
    dt_end = datetime.datetime.fromtimestamp(int(now + coffset))
    periods = len(pd.date_range(start=dt_now, end=dt_end, freq=resample, closed='left'))

    # Plot perf
    drange = mylib.date.getDateRangeFromEnd(nbdays, '1D')
    datascoins = dict()
    for coin in coins:
        data = mylib.commons.loadCoinHistorical(coin, drange, freq=resample)
        if len(data) > 0:
            data = analyzeDataPerf(data, periods)
            datascoins[coin] = data

    df = pd.DataFrame(mylib.commons.extractColumn(datascoins, 'perf_direction'))
    df[:-1].plot(subplots=True, grid=True, legend=True, kind='area', stacked=False)
    plt.show()

def getPerfCoinsDirection():
    # Parameters
    nbdays = mylib.conf.yanalyzer['analyze']['period'][0]['period']
    resample = mylib.conf.yanalyzer['analyze']['period'][0]['resample']
    compare = mylib.conf.yanalyzer['analyze']['period'][0]['compare']

    # Compute periods comparation offset
    now = mylib.date.getNow()
    coffset = pd.Timedelta('1D') / np.timedelta64(1, 's')
    dt_now = datetime.datetime.fromtimestamp(int(now))
    dt_end = datetime.datetime.fromtimestamp(int(now + coffset))
    periods = len(pd.date_range(start=dt_now, end=dt_end, freq=resample, closed='left'))

    # Plot perf
    drange = mylib.date.getDateRangeFromEnd(nbdays, '1D')
    datascoins = dict()
    for coin in coins:
        data = mylib.commons.loadCoinHistorical(coin, drange, freq=resample)
        if len(data) > 0:
            data = analyzeDataPerf(data, periods)
            datascoins[coin] = data


    df = pd.DataFrame(mylib.commons.extractColumn(datascoins, 'perf'))
    return df

def getcoinsPerf24h():
    # Parameters
    rewind = mylib.conf.yanalyzer['analyze']['period'][0]['rewind']
    resample = mylib.conf.yanalyzer['analyze']['period'][0]['resample']
    #compare = mylib.conf.yanalyzer['analyze']['period'][0]['compare']


    # Compute periods comparation offset
    now = mylib.date.getNow()
    coffset = pd.Timedelta(resample) / np.timedelta64(1, 's')
    dt_now = datetime.datetime.fromtimestamp(int(now))
    dt_end = datetime.datetime.fromtimestamp(int(now + coffset))
    periods = len(pd.date_range(start=dt_now, end=dt_end, freq=resample, closed='left'))

    datascoins = dict()
    for coin in coins:
        print('coin %s' % coin)
        data = mylib.commons.loadCoinHistorical2(coin, rewind=rewind, resample=resample)
        if len(data) > 0:
            #data = analyzeDataPerf(data, periods)
            datascoins[coin] = data

    df = pd.DataFrame(mylib.commons.extractColumn(datascoins, 'perf'))
    return df

def getcoinsPerf24h2():
    # Parameters
    rewind = mylib.conf.yanalyzer['analyze']['global']['rewind']
    resample = mylib.conf.yanalyzer['analyze']['period'][0]['resample']
    #compare = mylib.conf.yanalyzer['analyze']['period'][0]['compare']


    # Compute periods comparation offset
    now = mylib.date.getNow()
    coffset = pd.Timedelta(resample) / np.timedelta64(1, 's')
    dt_now = datetime.datetime.fromtimestamp(int(now))
    dt_end = datetime.datetime.fromtimestamp(int(now + coffset))
    periods = len(pd.date_range(start=dt_now, end=dt_end, freq=resample, closed='left'))

    datascoins = dict()
    for coin in coins:
        print('coin %s' % coin)
        data = mylib.commons.loadCoinHistorical2(coin, rewind=rewind, resample=resample)
        if len(data) > 0:
            #data = analyzeDataPerf(data, periods)
            datascoins[coin] = data

    df = pd.DataFrame(mylib.commons.extractColumn(datascoins, 'perf'))
    return df

def column_color(col):
    if 'perf_' in col.name:
        is_neg = col < 0
        return ['background-color: red' if v else 'background-color: green' for v in is_neg]

    if 'gain_' in col.name:
        is_neg = col < 0
        return ['color: red' if v else 'color: green' for v in is_neg]

    return [''] * len(col)

def negative_background(val):
    bg = ''
    if type(val) == float and val < 0:
        bg = 'background-color: red'

    return bg


def getMaxRewind():
    # Get max rewind period for loading data
    rewinds = []
    for period in mylib.conf.yanalyzer['analyze']['period']:
        rewinds.append(pd.Timedelta(period['rewind']))
    maxrewind = sorted(rewinds)[-1]

    return maxrewind

def summaryCoins(coins):

    # Sort period column
    periodcolumns = collections.OrderedDict()
    for period in mylib.conf.yanalyzer['analyze']['period']:
        periodcolumns[pd.Timedelta(period['resample'])] = period['name']

    datas = mylib.commons.loadAllCoinsHistorical3(coins, maxrewind)

    # Resample all coins historical datas
    periods = {}
    for period in mylib.conf.yanalyzer['analyze']['period']:
        print ("analyze %s with %s resample period" % (period['name'], period['resample']))
        periods[period['name']] = mylib.commons.resampleAllCoinsHistorical(datas, period['rewind'], period['resample'])

    # Compute columns values
    minperiodidx = list(periodcolumns)[0]
    minperiodname = periodcolumns[pd.Timedelta(minperiodidx)]
    column = {'firstdate':{}, 'lastdate': {}, 'nbdays': {}}
    for period in periods:
        columnperf = "perf_%s" % period
        column[columnperf] = {}
        if minperiodname == period:
            columnprice = "lastprice_%s" % minperiodname
            column[columnprice] = {}

        for coin in periods[period]:
            if len(periods[period][coin]) <= 0:
                continue

            if minperiodname == period:
                column[columnprice][coin] = periods[period][coin]['last'][-1]

            # Compute coins performance
            column[columnperf][coin] = {}

            # Search the first date for coin
            if coin not in column['firstdate']:
                column['firstdate'][coin] = periods[period][coin].index[0]
            column['firstdate'][coin] = min(periods[period][coin].index[0],column['firstdate'][coin])

            # Search the last date for coin
            if coin not in column['lastdate']:
                column['lastdate'][coin] = periods[period][coin].index[-1]
            column['lastdate'][coin] = max(periods[period][coin].index[-1],column['lastdate'][coin])

            column['nbdays'][coin] = column['lastdate'][coin] - column['firstdate'][coin]
            column[columnperf][coin] = periods[period][coin]['perf'][-1]

    columnname = []
    columnname.append("lastprice_%s" % minperiodname)
    for period in periodcolumns:
        columnname.append('perf_%s' % periodcolumns[period])
    # columnname.append('firstdate')
    # columnname.append('lastdate')
    columnname.append('nbdays')

    df = pd.DataFrame(column,columns=columnname)
    return df

def mySummaryCoin(df, rewind, resample):
    filtered = mylib.commons.filterHistorical(df, rewind)
    resampled = mylib.commons.resampleHistorical(filtered, resample)
    last = resampled.tail(1)

    # Compute missing datas
    now = datetime.datetime.now()
    lastdate = filtered.index[-1]
    firstdate = filtered.index[0]
    td_resample = pd.Timedelta(resample)
    # if td_resample < pd.Timedelta('0d'):
    #     td_resample = pd.Timedelta('0d')
    missingbefore = td_resample - (lastdate - firstdate)
    if missingbefore < pd.Timedelta('0d'):
        missingbefore = pd.Timedelta('0d')

    missingafter = now - lastdate
    if missingafter < pd.Timedelta('0d'):
        missingafter = pd.Timedelta('0d')

    df = pd.DataFrame(
        {
            'coin': last['coin'],
            'firstprice': last['last'],
            'lastprice': last['last'],
            'gain': last['last'] - last['first'],
            'perf': ((last['last'] / last['first']) - 1) * 100,
            'firstdate': firstdate,
            'lastdate': lastdate,
            'missingbefore': missingbefore,
            'missingafter': missingafter
        }
    )

    return df

def globalPerfCoins(markets, coins):
    summariescoins = []

    simulatemoney = mylib.conf.yanalyzer['analyze']['simulate']['money']

    for coin in coins:
        df = allcoins[coin]

        try:
            # 1H
            df1 = mySummaryCoin(df, '12h', '1h')
            df1 = df1.rename({
                'firstprice': 'firstprice_1H',
                'lastprice': 'lastprice_1H',
                'gain': 'gain_1H',
                'perf': 'perf_1H',
                'firstdate': 'firstdate_1H',
                'lastdate': 'lastdate_1H',
                'missingafter': 'missingafter_1H',
                'missingbefore': 'missingbefore_1H'},
                axis='columns'
            )
            df1['simulategain_1H'] = simulatemoney * (df1['perf_1H']/100)

            # 1D
            df2 = mySummaryCoin(df, '1d', '1d')
            df2 = df2.rename({
                'firstprice': 'firstprice_1D',
                'lastprice': 'lastprice_1D',
                'gain': 'gain_1D',
                'perf': 'perf_1D',
                'firstdate': 'firstdate_1D',
                'lastdate': 'lastdate_1D',
                'missingafter': 'missingafter_1D',
                'missingbefore': 'missingbefore_1D'},
                axis='columns'
            )
            df2['simulategain_1D'] = simulatemoney * (df2['perf_1D']/100)

            df = pd.merge(df1, df2, on='coin')
            summariescoins.append(df)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            pass

    try:
        df = pd.concat(summariescoins, axis=0)
        df.set_index('coin', inplace=True)

        count = len(df)
        perf1h = df['simulategain_1H'].sum() / (count*simulatemoney) * 100
        perf1d = df['simulategain_1D'].sum() / (count*simulatemoney) * 100
        gain1h = df['simulategain_1H'].sum()
        gain1d = df['simulategain_1D'].sum()
        missingbefore = df['missingbefore_1D'].max()
        missingafter = df['missingafter_1H'].min()


        lines1 = []
        lines1.append([["Number markets", len(markets)]])
        lines1.append([["Number coins for all markets", len(coins)]])

        lines2 = []
        lines2.append([["Gain1h", gain1h],["Perf1h", "%.2f" % perf1h]])
        lines2.append([["Gain1d", gain1d],["Perf1d", "%.2f" % perf1d]])
        lines2.append([["Missingbefore", missingbefore],["Missingafter", missingafter]])

        # Show Result
        text = mylib.text.getTitleText("Main coins informations")
        text += mylib.text.getLineText()
        text += mylib.text.convertArray2ColumnText(lines1)
        text += mylib.text.getLineTitleText("Coins performance")
        text += mylib.text.convertArray2ColumnText(lines2)
        text += mylib.text.getLineText()
        print(text)

    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        pass

def summaryPerfCoins(coins):
    summariescoins = []

    for coin in coins:
        df = allcoins[coin]

        # 1H
        df1 = mySummaryCoin(df, '12h', '1h')
        df1 = df1.rename({
            'firstprice': 'firstprice_1H',
            'lastprice': 'lastprice_1H',
            'gain': 'gain_1H',
            'perf': 'perf_1H',
            'firstdate': 'firstdate_1H',
            'lastdate': 'lastdate_1H',
            'missingafter': 'missingafter_1H',
            'missingbefore': 'missingbefore_1H'},
            axis='columns'
        )

        # 1D
        df2 = mySummaryCoin(df, '1d', '1d')
        df2 = df2.rename({
            'firstprice': 'firstprice_1D',
            'lastprice': 'lastprice_1D',
            'gain': 'gain_1D',
            'perf': 'perf_1D',
            'firstdate': 'firstdate_1D',
            'lastdate': 'lastdate_1D',
            'missingafter': 'missingafter_1D',
            'missingbefore': 'missingbefore_1D'},
            axis='columns'
        )
        df = pd.merge(df1, df2, on='coin')
        summariescoins.append(df)

    df = pd.concat(summariescoins, axis=0)
    df.set_index('coin', inplace=True)

    df[['perf_1H', 'perf_1D']] = df[['perf_1H', 'perf_1D']].round(2)

    s = df.style.apply(column_color)
    mylib.file.saveto('/tmp/result.html', str(s.render()).encode())


    # columns = []
    # columns.append([k for k in df.columns if 'perf_' in k])
    # df = df[columns]
    print (df)


mylib.commons.initCanalyzer()
markets = mylib.commons.getMarkets()
coins = mylib.commons.getCoins4Markets()
#coins = coins[:50]

good = 0
missing = 0
allcoins = {}

# Load all historical coins
maxrewind = getMaxRewind()
allcoins = mylib.commons.loadAllCoinsHistorical3(coins,maxrewind)

globalPerfCoins(markets, coins)
#summaryPerfCoins(coins)
sys.exit()

sys.exit()

# Summary Coins
df = summaryCoins(coins)
print (df.to_dict())
s = df.style.applymap(color_negative_red)
mylib.file.saveto('/tmp/result.html',str(s.render()).encode())
sys.exit()

df = getcoinsPerf24h2()
print ("Last datas: %s" % df.index[-1])
df.tail(1)
print (df)
sys.exit()

df[:-1].plot(subplots=True, grid=True, legend=True, kind='area', stacked=False)
plt.title('all coins perf for %s coins' % len(coins))
#plt.legend(['perf in %'])
plt.show()

# Points graphs
plotPoints(df)

# Prices graph
plotPrices(df)
