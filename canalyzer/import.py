# -*- coding: utf-8 -*-

import os
import re
import datetime

import yaml
from pymarketcap import Pymarketcap

import mylib.conf
import mylib.file
import mylib.date
import mylib.converter.coinmarketcap

coinmarketcap = Pymarketcap()

def getCacheDuration(cachename):
    cacheduration = mylib.date.humanDurationToSecond(mylib.conf.yanalyzer['import']['cache'][cachename])

    return cacheduration


def init():
    currentpath = os.path.dirname(os.path.abspath(__file__))

    path = "%s/results" % currentpath
    if not os.path.exists(path):
        os.makedirs(path)

    path = "%s/results/coins" % currentpath
    if not os.path.exists(path):
        os.makedirs(path)


def getLastCoinsInformation(coins):
    currentpath = os.path.dirname(os.path.abspath(__file__))
    filename = "%s/results/alllastcoins.json" % currentpath

    # Try read from cache
    lastcoinsinfo = mylib.file.loadJSON(filename,getCacheDuration('global'))
    if lastcoinsinfo:
        print ('Get all last coins from cache')
        return lastcoinsinfo

    lastcoinsinfo = []
    for coin in coins:
        try:
            # Create coin folder
            currentpath = os.path.dirname(os.path.abspath(__file__))
            coinpath = "%s/results/%s" % (currentpath, coin.upper())
            if not os.path.exists(coinpath):
                os.makedirs(coinpath)

            # Try read from cache
            filename = "%s/last.json" % coinpath
            lastcoin = mylib.file.loadJSON(filename,getCacheDuration('global'))
            if lastcoin:
                print ("Get last %s coin information from cache" % coin)
                lastcoinsinfo.append(lastcoin)
                mylib.file.saveJSON(filename,lastcoin)
                continue

            # Get coin info from coinmarketcap
            print ("Import last %s coin information" % coin)
            lastcoin = coinmarketcap.ticker(coin.upper())
            mylib.file.saveJSON(filename,lastcoin)
            lastcoinsinfo.append(lastcoin)
        except KeyError:
            pass

    return lastcoinsinfo

def importRange():
    for coin in mylib.conf.yanalyzer['analyze']:
        # Create folder if not exists
        currentpath = os.path.dirname(os.path.abspath(__file__))
        path = "%s/results/%s" % (currentpath, coin.upper())
        if not os.path.exists(path):
            os.makedirs(path)

        # Get period from import:daily yaml parameter
        oneday = int(mylib.date.humanDurationToSecond("1d"))
        nbdays = int(mylib.date.humanDurationToSecond(mylib.conf.yanalyzer['import']['daily']))
        end = int(mylib.date.getNow()) - oneday
        start = int(end - nbdays)

        # Download coins info
        for idx_ts in range(end, start, -oneday):
            ts = datetime.datetime.fromtimestamp(int(idx_ts))
            cdate = datetime.datetime(ts.year, ts.month, ts.day)

            datetext = "%02d-%02d-%02d" % (ts.year, ts.month, ts.day)
            filename = "%s/daily_%s.json" % (path, datetext)
            if not os.path.exists(filename):
                print ("Download %s stock info for %s" % (coin, datetext))
                stockinfo = coinmarketcap.historical(coin, cdate, cdate)
                if len(stockinfo) > 0:
                    mylib.converter.coinmarketcap.save_daily(filename,stockinfo[0])

def getCoins4Markets():
    currentpath = os.path.dirname(os.path.abspath(__file__))
    filename = "%s/results/coins2markets.json" % currentpath

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



init()
#importLast()
#importRange()

coinsID = getCoins4Markets()
coinsinfo = getLastCoinsInformation(coinsID)

print(coinsinfo)
