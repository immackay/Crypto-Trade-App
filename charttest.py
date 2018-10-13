#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 08:37:12 2017

@author: Ian
"""

import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import style
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

import pandas as pd
import numpy as np

style.use("ggplot")

width = 0.001

data = pd.read_csv("data/USDT_BTC.csv")
data = data[-60:-10]
data["datestamp"] = np.array(data["date"]).astype("datetime64[s]")
data['MPLDate'] = data['datestamp'].apply(lambda date: mdates.date2num(date.to_pydatetime()))
dates = data["datestamp"].tolist()
data = data.set_index('datestamp')
print("Data loaded")

a = plt.subplot2grid((8,6), (0,0), rowspan=5, colspan=6)
a2 = plt.subplot2grid((8,6), (6,0), rowspan=2, colspan=6, sharex=a)
print("Chart initialized")

csticks = candlestick_ohlc(a, data[["MPLDate","open","high","low","close"]].values, width, colorup="#00aa00", colordown="#aa0000")
print("OHLC")

#a2.fill_between(data['MPLDate'],0, data['volume'].values, facecolor = "#003388")
a2.bar(data['MPLDate'],data['volume'].values,width*2)
a2.set_ylabel("Volume")
a2.yaxis.set_major_locator(mticker.MaxNLocator(4))
print("Volume")

a.set_xticklabels([])
a.xaxis.set_major_locator(mticker.MaxNLocator(4))
a.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
for label in a2.xaxis.get_ticklabels():
        label.set_rotation(45)


plt.show()