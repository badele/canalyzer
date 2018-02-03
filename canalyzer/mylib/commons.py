# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import datetime
import collections

import mylib.conf
import mylib.file

import numpy as np
import pandas as pd

# Check configuration filename
workdir = os.getcwd()
conffilename = "%s/canalyzer.yaml" % workdir
if not os.path.exists(conffilename):
    print ("Please create %s configuration file")
    sys.exit(1)

# Path configurations
cachepath = 'canalyzer-cache'
tmppath = 'tmp'
rootpath = ""
coinspath = "coins"

def initCanalyzer():
    # tmp path
    path = getStoragePath(rootpath)
    if not os.path.exists(path):
        os.makedirs(path)

    # coins cache path
    path = getStoragePath(coinspath)
    if not os.path.exists(path):
        os.makedirs(path)

    pd.set_option('display.max_rows',None)
    pd.set_option('display.width',200)
    pd.set_option('display.float_format', lambda x: '%.5f' % x)


def getStoragePath(pathname, inccache=False):
    storagepath=cachepath
    if not inccache:
        storagepath = tmppath

    if pathname == "":
        return "%s/%s" % (workdir, storagepath)
    else:
        return "%s/%s/%s" % (workdir, storagepath, pathname)

def getCacheDuration():
    cacheduration = int(pd.Timedelta(mylib.conf.yanalyzer['cache']['duration'])/ np.timedelta64(1, 's'))

    return cacheduration



def getCoins4Markets(markets):
    """
    Get available coins for the markets from canalyzer.yaml file
    """
    filename = "%s/coins2markets.json" % getStoragePath(rootpath)

    if mylib.file.isInCache(filename):
        print ("Get coins4markets from cache")
        return mylib.file.loadJSON(filename)

    coins = []
    for market in markets:
        print ("Get coins for %s market" % market)
        coinmarketcap = mylib.conf.initCoinMarketCap()
        exchanges = coinmarketcap.exchange(market)
        for currencycoin in exchanges:
            m = re.match(r"([A-Z]+)\-([A-Z]+)",currencycoin['market'])
            if m:
                coin = m.group(1)
                currency = m.group(2)

                if currency in mylib.conf.yanalyzer['select']['currency']:
                    coins.append(coin)

    ignore = mylib.conf.yanalyzer['import']['ignore']
    filtered = [r for r in coins if r not in ignore]
    mylib.file.saveJSON(filename, filtered)

    return filtered

def importCoinsHistorical(coins,daterange):
    counterdate = len(daterange)
    for idx_date in daterange:
        counterdate -= 1
        countercoin = len(coins)
        for coin in coins:
            countercoin -= 1
            # If same date, not send to canalyzer-cache

            inccache = datetime.datetime.fromtimestamp(mylib.date.getNow()).date() != idx_date.date()
            coinpath = "%s/%s" % (getStoragePath(coinspath, inccache), coin.upper())
            if not os.path.exists(coinpath):
                os.makedirs(coinpath)

            dt_start = idx_date.replace(hour=0,minute=0, second=0,microsecond=0)
            dt_end = idx_date.replace(hour=23,minute=59, second=59,microsecond=999999)

            datetext = "%02d-%02d-%02d" % (dt_start.year, dt_start.month, dt_start.day)
            filename = "%s/daily_%s.json" % (coinpath, datetext)

            if inccache:
                # Check if exist in canalyzer-cache
                if os.path.exists(filename):
                    print ("File exist in canalyzer-cache for %s(%s)" % (coin, datetext))
                    continue
            else:
                # See if temporary file need update
                if mylib.file.isInCache(filename):
                    print ("File exist in temporary cache for %s(%s)" % (coin, datetext))
                    continue

            print ("C(%s)/D(%s) Download %s stock info for %s" % (countercoin, counterdate, coin, datetext))
            try:
                datas = {'date':[]}
                coinmarketcap = mylib.conf.initCoinMarketCap()
                coininfo = coinmarketcap.graphs.currency(coin,dt_start,dt_end)

                # Add date column and remove timestam on all keys
                for key in coininfo.keys():
                    datas[key] = []

                    if len(datas['date'])==0:
                        for line in coininfo[list(coininfo.keys())[0]]:
                            datas['date'].append(line[0])

                    for line in coininfo[key]:
                        datas[key].append(line[1])


                mylib.file.saveJSON(filename, datas)
            except (KeyboardInterrupt, SystemExit):
                raise

            except Exception:
                print ("ERROR => %s / %s / %s" % (coin,dt_start,dt_end))

            # coinmarketcap API limitation
            pausetime = 6
            print ("Coinmarketcap pause during %s seconds" % pausetime)
            time.sleep(pausetime)


# def loadCoinHistorical(coin, drange,freq='1H'):
#
#     datas = []
#     for ddate in drange:
#         # If same date, not send to cache
#         tocache = datetime.datetime.fromtimestamp(mylib.date.getNow()).date()!=ddate.date()
#         coinpath = "%s/%s" % (getStoragePath(coinspath, tocache), coin.upper())
#         if not os.path.exists(coinpath):
#             continue
#
#         datetext = "%02d-%02d-%02d" % (ddate.year, ddate.month, ddate.day)
#         filename = "%s/daily_%s.json" % (coinpath, datetext)
#
#         if not os.path.exists(filename):
#             continue
#
#         # Read historical coin
#         df = pd.read_json(filename)
#
#         if len(df) == 0:
#             continue
#
#         df.set_index('date', inplace=True)
#         df.index = df.index.tz_localize('UTC').tz_convert(mylib.conf.yanalyzer['conf']['timezone'])
#
#         # Resample and realign date
#         df = df.asfreq(freq=freq, method='bfill')
#         df.index = df.index.floor(freq)
#         datas.append(df)
#
#
#     if len(datas) == 0:
#         return pd.DataFrame()
#
#     df = pd.concat(datas)
#     df = df.sort_index()
#
#     return df

# def loadCoinHistorical2(coin, rewind, resample):
#
#     rewindfiledate = max(int(pd.Timedelta('1d')/ np.timedelta64(1, 's')), int(pd.Timedelta(rewind) / np.timedelta64(1, 's') * 2))
#     rangefiledate = mylib.date.getDateRangeFromEnd('%ss' % rewindfiledate, '1D')
#
#     datas = []
#     for ddate in rangefiledate:
#         # If same date, not send to cache
#         tocache = datetime.datetime.fromtimestamp(mylib.date.getNow()).date()!=ddate.date()
#         coinpath = "%s/%s" % (getStoragePath(coinspath, tocache), coin.upper())
#         if not os.path.exists(coinpath):
#             continue
#
#         datetext = "%02d-%02d-%02d" % (ddate.year, ddate.month, ddate.day)
#         filename = "%s/daily_%s.json" % (coinpath, datetext)
#
#         if not os.path.exists(filename):
#             continue
#
#         # Read historical coin
#         df = pd.read_json(filename)
#
#         if len(df) == 0:
#             continue
#
#         df.set_index('date', inplace=True)
#         #df.index = df.index.tz_localize('UTC').tz_convert(mylib.conf.yanalyzer['conf']['timezone'])
#         #df.index.tz = None
#
#         #r.index = r.index.floor(freq)
#         datas.append(df)
#
#     if len(datas) == 0:
#         return pd.DataFrame()
#
#     df = pd.concat(datas)
#     df = df.sort_index()
#
#     # Resample and realign date
#     r = df.resample(resample)
#     r = r.agg({
#         'price_usd': ['first', 'last', 'min', 'max'],
#         'volume_usd': ['mean']
#     })
#
#     r['gain'] = r['price_usd']['last'] - r['price_usd']['first']
#     r['perf'] = ((r['price_usd']['last'] / r['price_usd']['first']) - 1) * 100
#
#     # r.columns = r.columns.droplevel()
#     r = r.rename({'price_usd': 'price', 'volume_usd': 'volume'}, axis='columns')
#     r.columns = ['first','last','low','high','vol24','gain', 'perf']
#
#     # dfilter = datetime.datetime.now()
#     # filter = pd.date_range(start=dfilter,periods=3, freq='-%s' % resample)[2]
#     # print(pd.date_range(start=dfilter,periods=3, freq='-%s' % resample))
#     # print(r[r.index >= filter])
#
#     return r


def loadCoinHistorical(coin, rewind):

    print ("Load historical data for %s coin" % coin)

    # Minimal oneday
    minimalrewind = max(int(pd.Timedelta('1d')/ np.timedelta64(1, 's')), int(pd.Timedelta(rewind) / np.timedelta64(1, 's')))
    rangefiledate = mylib.date.getDateRangeFromEnd('%ss' % minimalrewind, '1D')

    datas = []
    for ddate in rangefiledate:
        # If same date, not send to cache
        tocache = datetime.datetime.fromtimestamp(mylib.date.getNow()).date()!=ddate.date()
        coinpath = "%s/%s" % (getStoragePath(coinspath, tocache), coin.upper())
        if not os.path.exists(coinpath):
            continue

        datetext = "%02d-%02d-%02d" % (ddate.year, ddate.month, ddate.day)
        filename = "%s/daily_%s.json" % (coinpath, datetext)

        if not os.path.exists(filename):
            continue

        # Read historical coin
        try:
            df = pd.read_json(filename)

            if len(df) == 0:
                continue

            df.set_index('date', inplace=True)
            #df.index = df.index.tz_localize('UTC').tz_convert(mylib.conf.yanalyzer['conf']['timezone'])
            #df.index.tz = None

            #r.index = r.index.floor(freq)
            datas.append(df)

        except ValueError:
            print("The %s is ignored, file bad format" % filename)
            pass

    if len(datas) == 0:
        return pd.DataFrame()

    df = pd.concat(datas)
    df['coin'] = coin
    df = df.sort_index()

    return df

def loadAllCoinsHistorical(coins, rewind):

    datas = {}
    for coin in coins:
        datas[coin] = loadCoinHistorical(coin,rewind)

    return datas


def filterHistorical(df,rewind):

    # Continue if no data in Dataframe
    if len(df) == 0:
        return pd.DataFrame()

    # filter data
    lastdate = df.index[-1]
    rewinddate = lastdate - pd.Timedelta(rewind)
    f = df[df.index >= rewinddate]

    return f


def resampleHistorical(df, resample):

    r = df.resample(resample)
    r = r.agg({
        'coin': ['last'],
        'price_usd': ['first', 'last', 'min', 'max'],
        'volume_usd': ['mean']
    })


    r['gain'] = r['price_usd']['last'] - r['price_usd']['first']
    r['perf'] = ((r['price_usd']['last'] / r['price_usd']['first']) - 1) * 100

    # r.columns = r.columns.droplevel()
    r = r.rename({'price_usd': 'price', 'volume_usd': 'volume'}, axis='columns')
    r.columns = ['coin', 'first','last','low','high','vol24','gain', 'perf']

    firstprice = float(r.head(1)['first'])
    simulatemoney = mylib.conf.yanalyzer['analyze']['simulate']['money']
    r['globalgain'] = r['last'] - firstprice
    r['globalperf'] = (r['last'] / firstprice-1)*100
    r = r.ffill().bfill()

    return r

def SumarizeHistorical(df, rewind, resample):
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


def resampleAllCoinsHistorical(datas,rewind, resample):

    result = {}
    for coin in datas:
        df = datas[coin]

        # Continue if no data in Dataframe
        if len(df) == 0:
            continue

        # filter data
        lastdate = df.index[-1]
        rewinddate = lastdate - pd.Timedelta(rewind)
        f = df[df.index >= rewinddate]

        # No more datas for computing summary
        if len(f)<1:
            continue

        r = f.resample(resample)
        r = r.agg({
            'price_usd': ['first', 'last', 'min', 'max'],
            'volume_usd': ['mean']
        })


        r['gain'] = r['price_usd']['last'] - r['price_usd']['first']
        r['perf'] = ((r['price_usd']['last'] / r['price_usd']['first']) - 1) * 100

        # r.columns = r.columns.droplevel()
        r = r.rename({'price_usd': 'price', 'volume_usd': 'volume'}, axis='columns')
        r.columns = ['first','last','low','high','vol24','gain', 'perf']

        selected = r.index[0].date() <= rewinddate.date()
        if selected:
            result[coin] = r
        else:
            result[coin] = pd.DataFrame()

    return result

def extractColumn(datas,column):

    extracted = dict()
    for key in datas:
        extracted[key] = datas[key][column]

    return extracted
