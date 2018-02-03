import pandas as pd

# Simple Moving Average
def SMA(s, n):
    r = s.rolling(n).mean()
    return r
