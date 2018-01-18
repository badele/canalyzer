# -*- coding: utf-8 -*-

import os
import re
import sys
import time
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

def importCoinsHistorical(coinmarketcap,coins,daterange):
    counterdate = len(daterange)
    for idx_date in daterange:
        counterdate -= 1
        countercoin = len(coins)
        for coin in coins:
            countercoin -= 1
            # If same date, not send to cache
            tocache = datetime.datetime.fromtimestamp(mylib.date.getNow()).date()!=idx_date.date()
            coinpath = "%s/%s" % (getStoragePath(coinspath, tocache), coin.upper())
            if not os.path.exists(coinpath):
                os.makedirs(coinpath)

            dt_start = idx_date.replace(hour=0,minute=0, second=0,microsecond=0)
            dt_end = idx_date.replace(hour=23,minute=59, second=59,microsecond=999999)

            datetext = "%02d-%02d-%02d" % (dt_start.year, dt_start.month, dt_start.day)
            filename = "%s/daily_%s.json" % (coinpath, datetext)
            if os.path.exists(filename):
                print ("File exist in the cache for %s(%s)" % (coin, datetext))
                continue

            print ("C(%s)/D(%s) Download %s stock info for %s" % (countercoin, counterdate, coin, datetext))
            try:
                datas = {'date':[]}
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


def loadCoinsHistorical(coins, drange):

    coinsID = coins
    if type(coins) == str:
        coinsID = [coins]


    datas4coins = []
    for coin in coinsID:
        # Download coins info

        datas4coin = []
        for ddate in drange:
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
            df = pd.read_json(filename)
            df['coin'] = coin
            datas4coin.append(df)

        if len(datas4coin) != len(drange):
            print ("ERROR loadCoinsHistorical for %s" % coin)
            continue

        # Add coin datas
        datas4coins.append(pd.concat(datas4coin))


    # Merge all historical coins
    df = pd.concat(datas4coins)

    # Reindex
    df.set_index('date', inplace=True)
    df.index = df.index.tz_localize('UTC').tz_convert(mylib.conf.yanalyzer['conf']['timezone'])
    df = df.sort_index()

    return df

