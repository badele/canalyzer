# -*- coding: utf-8 -*-

import os
import simplejson as json

import mylib.date
from mylib import commons

terminalheight, terminalwidth = os.popen('stty size', 'r').read().split()
terminalheight = int(terminalheight)
terminalwidth = int(terminalwidth)


def getTitleText(title):
    titlesize = len(title)

    count = mylib.text.terminalwidth - titlesize - 2
    lsize = int(count/2)

    return "%s %s\n" % (" "*lsize,title)

def getLineText(char='='):
    return "%s\n" % (char*mylib.text.terminalwidth)

def getLineTitleText(title, char="="):
    titlesize = len(title)

    count = mylib.text.terminalwidth - titlesize - 2
    lsize = int(count/2)
    rsize = mylib.text.terminalwidth - lsize - titlesize -2

    return "%s %s %s\n" % (char*lsize,title,char*rsize)


def convertArray2ColumnText(lines,columnspace=3):
    linestext = []
    for line in lines:
        colcount = len(line)

        # print empty line
        if colcount == 0:
            linestext.append("")
            continue

        colwidth = int(mylib.text.terminalwidth / colcount)
        modulospace = int(mylib.text.terminalwidth) % colcount

        text = ""
        idxcol = 1
        for colcontent in line:
            (name,value) = colcontent
            lenname = len("%s:" % name)
            lenvalue = len(str(value))

            # Reajust float division space
            addmodulospace = int(modulospace/float(colcount) * idxcol)
            addcolumnseparator = columnspace if idxcol<colcount else 0
            spacenamevalue = colwidth - addcolumnseparator - lenname - lenvalue

            text += "%s:%s%s%s%s" % (name," "*spacenamevalue," "*addmodulospace,str(value)," "*addcolumnseparator)

            idxcol += 1
        linestext.append(text)

    output = ""
    idxline = 1
    for line in linestext:
        output += "%s" % line
        if idxline < len(linestext):
            output += "\n"
        idxline += 1

    return output
    #'%-10s' '%s' % (s1, s2)
