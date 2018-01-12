# -*- coding: utf-8 -*-

import os
import simplejson as json

import mylib.date

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

def loadJSON(filename,cacheduration=0):
    if not os.path.exists(filename):
        return None

    now = mylib.date.getNow()
    ftime = os.path.getmtime(filename)

    if cacheduration == 0 or ftime + cacheduration > now:
        return json.load(open(filename, 'r'))

    return None
