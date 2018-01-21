# -*- coding: utf-8 -*-

import sys
import time
import datetime
from dateutil import tz
import pandas as pd

import mylib.conf

def getNow():
    now = datetime.datetime.now()
    ts = time.mktime(now.timetuple())

    return ts

def getDateRangeFromEnd(windows, humanperiod, enddate=None):

    if not enddate:
        enddate = datetime.datetime.now()
        #enddate = enddate.replace(tzinfo=None)

    (end, start) = pd.date_range(start=enddate, periods=2, freq='-%s' % windows).tz_localize(mylib.conf.yanalyzer['conf']['timezone'])

    return getDateRangeFromStartEnd(start, end, humanperiod)


def getDateRangeFromStartEnd(start, end, humanperiod):

    return pd.date_range(start=start, end=end, freq=humanperiod,closed='right')