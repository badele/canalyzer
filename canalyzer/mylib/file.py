# -*- coding: utf-8 -*-

import os
import simplejson as json

import mylib.date
from mylib import commons

def saveto(filename, content):
    """Save content to file"""

    # Create directory if not exists
    dirname = os.path.dirname(filename)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    # Write content
    out = open(filename, 'wb')
    out.write(content)
    out.close()

def saveJSON(filename, content):
    """Save JSON content to file"""

    json.dump(content, fp=open(filename, 'w'), indent=4)

def loadJSON(filename):
    return json.load(open(filename, 'r'))


def isInCache(filename):
    if not os.path.exists(filename):
        return False

    now = mylib.date.getNow()
    ftime = os.path.getmtime(filename)

    cacheduration = commons.getCacheDuration()
    if ftime + cacheduration < now:
        #os.remove(filename)
        return False

    return True
