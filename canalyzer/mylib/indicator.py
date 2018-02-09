# -*- coding: utf-8 -*-

import sys

import pandas as pd

import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.sandbox.regression.predstd import wls_prediction_std

# Simple Moving Average
def SMA(df, n):
    r = df.rolling(n).mean()

    return r

# Support Line
def SL(df, o):

    idxpoint = df.index >= pd.to_datetime(o['point'])
    value = float(df[idxpoint].head(1))
    return HL(df,value)


# Horizontal Line
def HL(df, value):
    r = df.copy()
    r = value

    return r

def trend_line(df,o):
    x = []
    y = []

    boxstart = df.index >= pd.to_datetime(o['box']['start'])
    boxend = df.index >= pd.to_datetime(o['box']['end'])

    idxboxstart = np.argmax(boxstart)
    idxboxend = np.argmax(boxend)

    # Search x0 value
    selectors = df.index >= pd.to_datetime(o['point']['first'])
    x.append(np.argmax(selectors))
    y.append(float(df.loc[selectors].head(1)))

    # Search x1 value
    selectors = df.index >= pd.to_datetime(o['point']['second'])
    x.append(np.argmax(selectors))
    y.append(float(df.loc[selectors].head(1)))

    # Compute Linear function
    a = (y[1] - y[0])/(x[1] - x[0])
    b = y[0] - x[0]*a

    # fill with linear function
    fx = np.arange(len(df))
    fy = fx*a+b

    # Only draw in box limit
    fy[fx<idxboxstart] = np.nan
    fy[fx>idxboxend] = np.nan

    return fy

# Linear Regression
def LR(df,options):
    srcsize = len(df)

    n = 0
    if 'divisor' in options:
        n = int(srcsize / options['divisor'])

    # Resize for Linear Regression computin
    if n != 0:
        df = df.tail(n)

    x = np.arange(len(df))

    res = sm.OLS(df,x).fit()

    std, lower, upper = wls_prediction_std(res)
    middle = res.predict()

    nfill = srcsize - n
    if nfill != srcsize:
        empty = np.full_like(np.arange(nfill), np.nan, dtype=np.double)
        std = np.append(empty,std)
        lower = np.append(empty,lower)
        upper = np.append(empty,upper)
        middle = np.append(empty,middle)

    return std, middle, lower, upper

# Linear Regression
def LR2(df,options):
    srcsize = len(df)

    n = 0
    if 'divisor' in options:
        n = int(srcsize / options['divisor'])

    # Resize for Linear Regression computin
    if n != 0:
        df = df.tail(n)

    x = np.arange(len(df))
    X = np.column_stack((x, x**2))
    X = sm.add_constant(X)

    res = sm.OLS(df,X).fit()

    std, lower, upper = wls_prediction_std(res)
    middle = res.predict()

    nfill = srcsize - n
    if nfill != srcsize:
        empty = np.full_like(np.arange(nfill), np.nan, dtype=np.double)
        std = np.append(empty,std)
        lower = np.append(empty,lower)
        upper = np.append(empty,upper)
        middle = np.append(empty,middle)

    return std, middle, lower, upper
