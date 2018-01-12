# -*- coding: utf-8 -*-

import os
import re
import datetime

import yaml
from pymarketcap import Pymarketcap

import numpy as np

import mylib.conf
import mylib.file
import mylib.date
import mylib.converter.coinmarketcap

coinmarketcap = Pymarketcap()

def getCacheDuration(cachename):
    cacheduration = mylib.date.humanDurationToSecond(mylib.conf.yanalyzer['import']['cache'][cachename])

    return cacheduration

def initCanalyzer():
    currentpath = os.path.dirname(os.path.abspath(__file__))
    path = "%s/tmp" % currentpath
    if not os.path.exists(path):
        os.makedirs(path)

def getCoins4Markets():
    """
    Get available coins for the markets from canalyzer.yaml file
    """
    currentpath = os.path.dirname(os.path.abspath(__file__))
    filename = "%s/tmp/coins2markets.json" % currentpath

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


def getLastCoinsInformation(coins):
    currentpath = os.path.dirname(os.path.abspath(__file__))
    filename = "%s/tmp/alllastcoins.json" % currentpath

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
            coinpath = "%s/tmp/coins/%s" % (currentpath, coin.upper())
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

def importCoinsHistorical(coins):
    for coin in coins:
        # Create folder if not exists
        currentpath = os.path.dirname(os.path.abspath(__file__))
        coinpath = "%s/canalyzer-cache/coins/%s" % (currentpath, coin.upper())
        if not os.path.exists(coinpath):
            os.makedirs(coinpath)

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
            filename = "%s/daily_%s.json" % (coinpath, datetext)
            if not os.path.exists(filename):
                print ("Download %s stock info for %s" % (coin, datetext))
                try:
                    stockinfo = coinmarketcap.historical(coin, cdate, cdate)
                    if len(stockinfo) > 0:
                        mylib.converter.coinmarketcap.save_daily(filename,stockinfo[0])
                except (KeyboardInterrupt, SystemExit):
                    raise

                except:
                    pass

def analyseAllCoinsPerf(coins,nbdays=1):
    oneday = int(mylib.date.humanDurationToSecond("1d"))
    end = int(mylib.date.getNow()) - oneday
    dend = datetime.datetime.fromtimestamp(int(end))
    dstart = dend - datetime.timedelta(days=nbdays)


    tstart = datetime.datetime(dstart.year, dstart.month, dstart.day)
    datetext = "%02d-%02d-%02d" % (tstart.year, tstart.month, tstart.day)
    startfilename = "daily_%s.json" % datetext

    tend = datetime.datetime(dend.year, dend.month, dend.day)
    datetext = "%02d-%02d-%02d" % (tend.year, tend.month, tend.day)
    endfilename = "daily_%s.json" % datetext

    sumstart = []
    sumend = []
    for coin in coins:
        try:
            currentpath = os.path.dirname(os.path.abspath(__file__))
            coinpath = "%s/canalyzer-cache/coins/%s" % (currentpath, coin.upper())

            # Search we have two history
            startfullname = "%s/%s" % (coinpath, startfilename)
            endfullname = "%s/%s" % (coinpath, endfilename)
            if not os.path.exists(startfullname) or not os.path.exists(endfullname):
                continue

            jstart = mylib.file.loadJSON(startfullname)
            jend = mylib.file.loadJSON(endfullname)


            sumstart.append(jstart['close'])
            sumend.append(jend['close'])

        except (KeyboardInterrupt, SystemExit):
            raise


    nstart = np.sum(np.array(sumstart))
    nend = np.sum(np.array(sumend))
    ratio = ((nend/nstart)-1)*100

    marketcount = len(mylib.conf.yanalyzer['select']['market'])
    coincount = 0
    for market in mylib.conf.yanalyzer['select']['market']:
        try:
            exchanges = coinmarketcap.exchange(market)
            coincount += len(exchanges)
        except:
            pass

    print ("%.02f %% trend for %s market(s) and %s coin(s)" % (ratio, marketcount, coincount))

initCanalyzer()

coinsID = getCoins4Markets()
#getLastCoinsInformation(coinsID)
#importCoinsHistorical(coinsID)
analyseAllCoinsPerf(coinsID)

#coinsinfo = getLastCoinsInformation(coinsID)
#print(coinsinfo)
