# -*- coding: utf-8 -*-

import time
import datetime

def getNow():
    now = datetime.datetime.now()
    ts = time.mktime(now.timetuple())

    return ts

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
