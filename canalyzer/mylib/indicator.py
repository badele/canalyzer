# -*- coding: utf-8 -*-

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
def LR(df):
    x = np.arange(len(df))
    X = np.column_stack((x, x**2))
    X = sm.add_constant(X)

    res = sm.OLS(df,X).fit()
    print(res.summary())

    std, lower, upper = wls_prediction_std(res)
    middle = res.predict()
    print (middle)

    return std, middle, lower, upper
