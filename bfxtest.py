import pandas as pd
import numpy as np
import urllib, json

def v1():
    dataLink = "https://api.bitfinex.com/v1/trades/BTCUSD?limit_trades=2000"
    data = urllib.request.urlopen(dataLink)
    data = data.read().decode("utf-8")
    data = json.loads(data)
    
    data = pd.DataFrame(data)
    
    buys = data[(data["type"]=="buy")]   
    buys["datestamp"]= np.array(buys["timestamp"]).astype("datetime64[s]")
    buyDates = (buys["datestamp"]).tolist()
    
    sells = data[(data["type"]=="sell")]
    
    sells["datestamp"]= np.array(sells["timestamp"]).astype("datetime64[s]")
    sellDates = (sells["datestamp"]).tolist()

    return buys, buyDates, sells, sellDates

def v2():
    dataLink = "https://api.bitfinex.com/v2/trades/tBTCUSD/hist?limit_trades=2000"
    data = urllib.request.urlopen(dataLink)
    data = data.read().decode("utf-8")
    data = json.loads(data)
    
    data = pd.DataFrame(data)
    
    buys = data[(data[2]>0)]
    
    buys["datestamp"]= np.array(buys[1]).astype("datetime64[s]")
    buyDates = (buys["datestamp"]).tolist()
    
    sells = data[(data[2]<0)]
    
    sells["datestamp"]= np.array(sells[1]).astype("datetime64[s]")
    sellDates = (sells["datestamp"]).tolist()

    return buys, buyDates, sells, sellDates

b1, bd1, s1, sd1 = v1()

#print("Buys:")
#print(b1.tail())
#for i in bd1[-5:]:
#    print(i)

print("Sells:")
print(s1.head())
for i in sd1[:5]:
    print(i)

print("\n\nV2:")
dataLink = "https://api.bitfinex.com/v2/trades/tBTCUSD/hist?limit_trades=2000"
data = urllib.request.urlopen(dataLink)
data = data.read().decode("utf-8")
data = json.loads(data)
    
data = pd.DataFrame(data)
    
#buys = data[(data[2]>0)]
sells = data[(data[2]<0)]
sells[1] = sells[1]/1000
#for i in sells:
#    sells = (i[1]/1000)
#print(buys.head())
print(sells.head())
print(sells[1].head().astype("datetime64[s]"))
"""
b2, bd2, s2, sd2 = v2()
print("Buys2:")
print(b2.tail())
for i in bd2[-5:]:
    print(i)

print("Sells2:")
print(s2.tail())
for i in sd2[-5:]:
    print(i)
"""
