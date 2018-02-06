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

# Linear Regression
def LR(df,n=0):
    srcsize = len(df)

    # Resize for Linear Regression computin
    if n != 0:
        df = df.tail(n)

    x = np.arange(len(df))

    res = sm.OLS(df,x).fit()
    print(res.summary())

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
def LR2(df,n=0):
    srcsize = len(df)

    # Resize for Linear Regression computin
    if n != 0:
        df = df.tail(n)

    x = np.arange(len(df))
    X = np.column_stack((x, x**2))
    X = sm.add_constant(X)

    res = sm.OLS(df,X).fit()
    print(res.summary())

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
