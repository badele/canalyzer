# -*- coding: utf-8 -*-

import time
import datetime

def getNow():
    now = datetime.datetime.now()
    ts = time.mktime(now.timetuple())

    return ts

def getFilenameDateRange(humanperiod):
    seconds = int(humanDurationToSecond(humanperiod))

    dt_end = datetime.datetime.now()
    dt_start = dt_end - datetime.timedelta(seconds=seconds)

    dt_start = dt_start.replace(hour=0, minute=0, second=0, microsecond=0)
    dt_end = dt_end.replace(hour=0, minute=0, second=0, microsecond=0)

    print (dt_start)
    print (dt_end)

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
