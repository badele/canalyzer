# -*- coding: utf-8 -*-

import yaml
from pymarketcap import Pymarketcap

import mylib.file
import mylib.date
import mylib.converter.coinmarketcap

# init
fanalyzer = open("canalyzer.yaml", "r")
yanalyzer = yaml.load(fanalyzer)
