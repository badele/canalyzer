# -*- coding: utf-8 -*-

import os
import simplejson as json

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