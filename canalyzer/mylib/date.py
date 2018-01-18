# -*- coding: utf-8 -*-

import sys
import time
import datetime
import pandas as pd

def getNow():
    now = datetime.datetime.now()
    ts = time.mktime(now.timetuple())

    return ts

def getDateRangeFromEnd(windows, humanperiod, enddate=None):

    if not enddate:
        enddate = datetime.datetime.now()

    (end, start) = pd.date_range(start=enddate, periods=2, freq='-%s' % windows)

    return getDateRangeFromStartEnd(start, end, humanperiod)


def getDateRangeFromStartEnd(start, end, humanperiod):

    return pd.date_range(start=start, end=end, freq=humanperiod,closed='right')

#
def humanDurationToSecond(duration):

    durations = {
    's': 1,
    'm': 60,
    'h': 60 * 60,
    'd': 24 * 60 * 60,
    }


    value = duration[0:-1]
    timename = duration[-1]
    multiplicator = 1

    if timename in durations:
        multiplicator = durations[timename]


    seconds = int(value) * multiplicator

    return seconds
