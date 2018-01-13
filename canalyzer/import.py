# -*- coding: utf-8 -*-

import os

from pymarketcap import Pymarketcap

from mylib import commons


# def getLastCoinsInformation(coins):
#     filename = "%s/tmp/alllastcoins.json" % currentpath
#
#     # Try read from cache
#     lastcoinsinfo = mylib.file.loadJSON(filename,getCacheDuration('global'))
#     if lastcoinsinfo:
#         print ('Get all last coins from cache')
#         return lastcoinsinfo
#
#     lastcoinsinfo = []
#     for coin in coins:
#         try:
#             # Create coin folder
#             coinpath = "%s/tmp/coins/%s" % (currentpath, coin.upper())
#             if not os.path.exists(coinpath):
#                 os.makedirs(coinpath)
#
#             # Try read from cache
#             filename = "%s/last.json" % coinpath
#             lastcoin = mylib.file.loadJSON(filename,getCacheDuration('global'))
#             if lastcoin:
#                 print ("Get last %s coin information from cache" % coin)
#                 lastcoinsinfo.append(lastcoin)
#                 mylib.file.saveJSON(filename,lastcoin)
#                 continue
#
#             # Get coin info from coinmarketcap
#             print ("Import last %s coin information" % coin)
#             lastcoin = coinmarketcap.ticker(coin.upper())
#             mylib.file.saveJSON(filename,lastcoin)
#             lastcoinsinfo.append(lastcoin)
#         except KeyError:
#             pass
#
#     return lastcoinsinfo

# def importCoinsHistorical(coins):
#     for coin in coins:
#         # Create folder if not exists
#         currentpath = os.path.dirname(os.path.abspath(__file__))
#         coinpath = "%s/canalyzer-cache/coins/%s" % (currentpath, coin.upper())
#         if not os.path.exists(coinpath):
#             os.makedirs(coinpath)
#
#         # Get period from import:daily yaml parameter
#         oneday = int(mylib.date.humanDurationToSecond("1d"))
#         nbdays = int(mylib.date.humanDurationToSecond(mylib.conf.yanalyzer['import']['nbdays']))
#         end = int(mylib.date.getNow()) - oneday
#         start = int(end - nbdays)
#
#         # Download coins info
#         for idx_ts in range(end, start, -oneday):
#             ts = datetime.datetime.fromtimestamp(int(idx_ts))
#             cdate = datetime.datetime(ts.year, ts.month, ts.day)
#
#             datetext = "%02d-%02d-%02d" % (ts.year, ts.month, ts.day)
#             filename = "%s/daily_%s.json" % (coinpath, datetext)
#             if not os.path.exists(filename):
#                 print ("Download %s stock info for %s" % (coin, datetext))
#                 try:
#                     stockinfo = coinmarketcap.historical(coin, cdate, cdate)
#                     if len(stockinfo) > 0:
#                         mylib.converter.coinmarketcap.save_daily(filename,stockinfo[0])
#                 except (KeyboardInterrupt, SystemExit):
#                     raise
#
#                 except:
#                     pass




commons.initCanalyzer()

coinmarketcap = Pymarketcap()
coinsID = commons.getCoins4Markets(coinmarketcap)
#getLastCoinsInformation(coinsID)
commons.importCoinsHistorical(coinmarketcap,coinsID)
#analyseAllCoinsPerf(coinsID)

#coinsinfo = getLastCoinsInformation(coinsID)
#print(coinsinfo)
