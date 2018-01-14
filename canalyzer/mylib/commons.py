# -*- coding: utf-8 -*-

import os
import re
import sys
import datetime

import mylib.conf
import mylib.file

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

    pd.set_option('display.width',200)
    pd.set_option('display.float_format', lambda x: '%.5f' % x)


def getStoragePath(pathname, sendCache=False):
    storagepath=cachepath
    if not sendCache:
        storagepath = tmppath

    if pathname == "":
        return "%s/%s" % (workdir, storagepath)
    else:
        return "%s/%s/%s" % (workdir, storagepath, pathname)

def getCacheDuration(cachename):
    cacheduration = mylib.date.humanDurationToSecond(mylib.conf.yanalyzer['cache']['duration'])

    return cacheduration

def getCoins4Markets(coinmarketcap):
    """
    Get available coins for the markets from canalyzer.yaml file
    """
    filename = "%s/coins2markets.json" % getStoragePath(rootpath)
    coins2markets = mylib.file.loadJSON(filename,getCacheDuration('global'))
    if coins2markets:
        print ("Get coins4markets from cache")
        return coins2markets

    coins = []
    for market in mylib.conf.yanalyzer['select']['market']:
        print ("Get coins for %s market" % market)
        exchanges = coinmarketcap.exchange(market)
        for currencycoin in exchanges:
            m = re.match(r"([A-Z]+)\-([A-Z]+)",currencycoin['market'])
            if m:
                coin = m.group(1)
                currency = m.group(2)

                if currency in mylib.conf.yanalyzer['select']['currency']:
                    coins.append(coin)
    mylib.file.saveJSON(filename, coins)

    return coins

def importCoinsHistorical(coinmarketcap,coins):
    for coin in coins:
        # Get period from import:daily yaml parameter
        oneday = int(mylib.date.humanDurationToSecond("1d"))
        nbdays = int(mylib.date.humanDurationToSecond(mylib.conf.yanalyzer['import']['nbdays']))
        ts_end = int(mylib.date.getNow())
        ts_start = int(ts_end - nbdays)

        # Download coins info
        for idx_ts in range(ts_end, ts_start, -oneday):
            dt = datetime.datetime.fromtimestamp(int(idx_ts))

            # If same date, not send to cache
            tocache = datetime.datetime.fromtimestamp(mylib.date.getNow()).date()!=dt.date()
            coinpath = "%s/%s" % (getStoragePath(coinspath, tocache), coin.upper())
            if not os.path.exists(coinpath):
                os.makedirs(coinpath)

            dt_start = dt.replace(hour=0,minute=0, second=0,microsecond=0)
            dt_end = dt.replace(hour=23,minute=59, second=59,microsecond=999999)

            datetext = "%02d-%02d-%02d" % (dt_start.year, dt_start.month, dt_start.day)
            filename = "%s/daily_%s.json" % (coinpath, datetext)
            if os.path.exists(filename):
                print ("File exist in the cache for %s(%s)" % (coin, datetext))
                continue

            print ("Download %s stock info for %s" % (coin, datetext))
            try:
                datas = {'date':[]}
                coininfo = coinmarketcap.graphs.currency("ETH",dt_start,dt_end)

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

                # except:
                #     pass

            # coinmarketcap.graphs.currency("BTC")
            #
            # cdate = datetime.datetime(ts.year, ts.month, ts.day)
            #
            # datetext = "%02d-%02d-%02d" % (ts.year, ts.month, ts.day)
            # filename = "%s/daily_%s.json" % (coinpath, datetext)
            # if not os.path.exists(filename):
            #     print ("Download %s stock info for %s" % (coin, datetext))
            #     try:
            #         stockinfo = coinmarketcap.historical(coin, cdate, cdate)
            #         if len(stockinfo) > 0:
            #             mylib.converter.coinmarketcap.save_daily(filename,stockinfo[0])
            #     except (KeyboardInterrupt, SystemExit):
            #         raise
            #
            #     except:
            #         pass

def loadCoinHistorical(coin,nbdays):
    # Get period from import:daily yaml parameter
    oneday = int(mylib.date.humanDurationToSecond("1d"))
    nbdays = int(mylib.date.humanDurationToSecond(nbdays))
    ts_end = int(mylib.date.getNow())
    ts_start = int(ts_end - nbdays)

    # Download coins info
    datas = []
    for idx_ts in range(ts_end, ts_start, -oneday):
        dt = datetime.datetime.fromtimestamp(int(idx_ts))

        # If same date, not send to cache
        tocache = datetime.datetime.fromtimestamp(mylib.date.getNow()).date()!=dt.date()
        coinpath = "%s/%s" % (getStoragePath(coinspath, tocache), coin.upper())
        if not os.path.exists(coinpath):
            continue

        dt_start = dt.replace(hour=0,minute=0, second=0,microsecond=0)

        datetext = "%02d-%02d-%02d" % (dt_start.year, dt_start.month, dt_start.day)
        filename = "%s/daily_%s.json" % (coinpath, datetext)

        df = pd.read_json(filename)

        datas.append(df)

    df = pd.concat(datas)
    df['coin'] = coin

    df.set_index('date', inplace=True)
    df.index = df.index.tz_localize('UTC').tz_convert(mylib.conf.yanalyzer['conf']['timezone'])
    df = df.sort_index()

    return df