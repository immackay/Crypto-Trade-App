import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import pandas as pd
import numpy as np

import multiprocessing as mp
import urllib, json, os, datetime, configparser, ast
from functools import partial

CONFIG = "TAConfig.cfg"
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)

EXCHANGES = [['bfx','Bitfinex'],['bsp','Bitstamp'],['gdax','GDAX/Coinbase'],
            ['krk','Kraken'],['qcx','QuadrigaCX'],['bhb','Bithumb'],
            ['okc','OKCoin'],['hbi','Huobi'],['bcc','BTCChina'],['bfl','bitFlyer']]
exchange = EXCHANGES[0]
pair = "BTCUSD"

updateinterval = 5000
minute = 60000
hour = minute * 60
day = hour * 24
week = day * 7
TIMEFRAMES = [['t','Tick',updateinterval],['1m','1 Minute',minute],['5m','5 Minutes',5*minute],['15m','15 Minutes',15*minute],
            ['30m','30 Minutes',30*minute],['1h','1 Hour',hour],['2h','2 Hours',2*hour],['4h','4 Hours',4*hour],
            ['6h','6 Hours',6*hour],['12h','12 Hours',12*hour],['1d','1 Day',day],['3d','3 Days',3*day],
            ['1w','1 Week',week],['2w','2 Weeks',2*week],['4w','1 Month',4*week]]
timeframe = TIMEFRAMES[10]
samplesize = TIMEFRAMES[3]
candlewidth = ((samplesize[2]/timeframe[2])*0.8)

INDICATORS = {'sma':{'labels':['Periods'],'defaults':[10]},'ema':{'labels':['Periods'],'defaults':[10]},
            'rsi':{'labels':['Periods'],'defaults':[10]},'macd':{'labels':['EMA L','EMA S','Signal'],'defaults':[26,12,9]}}
indicators = {'top':[],'graph':[],'bottom':[]}

datastream = True
scale = 'lin'

style.use("fivethirtyeight")
f = Figure()
a = f.add_subplot(111)

# Chart defs
def bfx():
    dataLink = "https://api.bitfinex.com/v2/trades/tBTCUSD/hist?limit_trades=10000"
    data = urllib.request.urlopen(dataLink)
    data = data.read().decode("utf-8")
    data = json.loads(data)
    data = pd.DataFrame(data)
    # Reverse data, make unix timestamps proper size and make new column for datestamp
    data = data.reindex(index=data.index[::-1])
    data[1] = data[1]/1000
    data[4] = np.array(data[1]).astype("datetime64[s]")
    return data

def Animate(i):
    data = bfx()
    # Separate buys and sells
    buys = data[(data[2]>0)]
    buyDates = (buys[4]).tolist()
    sells = data[(data[2]<0)]
    sellDates = (sells[4]).tolist()

    # Plot buys and sells
    a.clear()
    a.plot_date(buyDates, buys[3], "g", label="Buys")
    a.plot_date(sellDates,sells[3], "r", label="Sells")
    title = "{} {}\nLast Price: {}".format(exchange[1],pair,data[3][-1:].item())
    a.set_title(title)
    a.legend(bbox_to_anchor=(0, 1.02, 1, 0.102), loc=3,
             ncol=2, borderaxespad=0)

def Stream():
    global datastream
    if datastream:
        datastream = False
        print("Datastream paused")
    else:
        datastream = True
        print("Datastream resumed")

def Scale():
    global scale
    if scale=='lin':
        scale = 'log'
        print("Switched to logarithmic scale")
    else:
        scale = 'lin'
        print("Switched to linear scale")

# Application commands
def Quit():
    app.destroy()

def Config(cmd):
    config = configparser.ConfigParser()
    global exchange
    global pair
    global timeframe
    global samplesize
    global candlewidth
    global indicators
    global scale
    if cmd=='save':
        config['CONFIG'] = {'EXCHANGE':exchange,'PAIR':pair,'TIMEFRAME':timeframe,
        'SAMPLESIZE':samplesize,'CANDLEWIDTH':candlewidth,'INDICATORS':indicators,'SCALE':scale}
        with open(CONFIG,"w") as c:
            config.write(c)
        Popup("Config saved!")
    elif cmd=='load':
        config.read(CONFIG)
        exchange = ast.literal_eval(config['CONFIG']['EXCHANGE'])
        pair = config['CONFIG']['PAIR']
        timeframe = ast.literal_eval(config['CONFIG']['TIMEFRAME'])
        samplesize = ast.literal_eval(config['CONFIG']['SAMPLESIZE'])
        candlewidth = ast.literal_eval(config['CONFIG']['CANDLEWIDTH'])
        indicators = ast.literal_eval(config['CONFIG']['INDICATORS'])
        scale = config['CONFIG']['SCALE']
        Popup("Config loaded!")

def Popup(msg):
    popup = tk.Tk()
    popup.wm_title("!!!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()

# Configuration commands
def ChangeExchange(e):
    global exchange
    global updateinterval

    exchange = e
    updateinterval = 5000
    print("Changed exchange to {}".format(exchange))

def ChangeTimeFrame(tf=timeframe,ss=samplesize):
    global timeframe
    global samplesize
    global candlewidth
    if tf in TIMEFRAMES[-3:] and ss in TIMEFRAMES[:3]:
        Popup("Too much data chosen, choose a smaller time frame or a larger sample size")
    else:
        timeframe = tf
        samplesize = ss
        candlewidth = ((samplesize[2]/timeframe[2])*0.8)
        print("Changed timeframe to {}, samplesize to {}, candlewidth is {}".format(timeframe,samplesize,candlewidth))

def AddIndicator(ind, loc):
    if samplesize==TIMEFRAMES[0]:
        Popup("Indicators not available with tick data")
        pass
    elif ind in ('sma','ema') and loc in ('top','bottom') or ind in ('macd','rsi') and loc=='graph':
        Popup("Error")
    else:
        prompt = tk.Tk()
        prompt.wm_title("Indicator Setup")
        x = 0
        entry = {}

        for l in INDICATORS[ind]['labels']:
            label = tk.Label(prompt, text="{}:".format(l))
            label.grid(row=x,column=0,padx=5,pady=5,sticky=tk.E+tk.W)
            e = tk.Entry(prompt)
            entry[x] = e
            e.insert(0,INDICATORS[ind]['defaults'][x])
            e.grid(row=x,column=1,sticky=tk.E+tk.W)
            x+=1
        entry[0].focus_set()

        def callback():
            global indicators
            ilist = dict(indicators[loc])
            mod = []
            for e in entry:
                x = entry[e].get()
                mod.append(x)
            j = 0
            for y in range(len([i for i in ilist])):
                if '{}{}'.format(ind,y) not in ilist:
                    j = y
                    break
            ilist.update({'{}{}'.format(ind,j): mod})
            print("Added {} indicator with modifiers ({}) to {} location".format(ind,mod,loc))
            prompt.destroy()

        b = tk.Button(prompt,text="Submit",width=10,command=callback)
        b.grid(row=x,column=0,columnspan=2)
        tk.mainloop()

def RemIndicator(ind, loc):
    pass

class TradeApp(tk.Tk):
    def __init__(self,*args,**kwargs):
        # TKinter initialization, window icon and title
        tk.Tk.__init__(self,*args,**kwargs)
        icon = tk.PhotoImage(file="clienticon.gif")
        self.tk.call('wm','iconphoto',self._w,icon)
        tk.Tk.wm_title(self,"Crypto Trader")
        # Initial container
        container = tk.Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=0)
        container.grid_columnconfigure(1, weight=1)
        # Menubar stuff
        menubar = MenuBar(container)
        tk.Tk.config(self, menu=menubar)
        # Initialize pages, open startpage
        self.frames = {}
        sp = StartPage(container, self)
        self.frames[StartPage] = sp
        sp.grid(row=0,column=0,columnspan=2,sticky="nsew")
        bb = ButtonBar(container, self)
        self.frames[ButtonBar] = bb
        bb.grid(row=0,column=0,sticky="nsw")
        for F in (GraphPage, TradePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0,column=1,sticky="nsew")
        if os.path.exists(CONFIG):
            self.show_frame(ButtonBar)
            self.show_frame(GraphPage)
        else:
            self.show_frame(StartPage)

    def show_frame(self,controller):
        frame = self.frames[controller]
        frame.tkraise()

class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        filemenu = tk.Menu(self, tearoff=0)
        filemenu.add_command(label="Save config", command=partial(Config,'save'))
        filemenu.add_command(label="Load config", command=partial(Config,'load'))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=Quit)

        exchangemenu = tk.Menu(self, tearoff=1)
        for e in EXCHANGES:
            exchangemenu.add_command(label=e[1], command=partial(ChangeExchange,e))

        timeframemenu = tk.Menu(self, tearoff=1)
        for t in TIMEFRAMES[4:]:
            timeframemenu.add_command(label=t[1], command=partial(ChangeTimeFrame,tf=t))

        samplesizemenu = tk.Menu(self, tearoff=1)
        for s in TIMEFRAMES:
            samplesizemenu.add_command(label=s[1], command=partial(ChangeTimeFrame,ss=s))

        # Sentdex garbage
        indicatormenu = tk.Menu(self, tearoff=1)
        indicatormenu.add_command(label="-----Top-----", state=tk.DISABLED)
        indicatormenu.add_command(label="None")
        indicatormenu.add_command(label="RSI", command=partial(AddIndicator,'rsi','top'))
        indicatormenu.add_command(label="MACD", command=partial(AddIndicator,'macd','top'))

        indicatormenu.add_command(label="----Graph----", state=tk.DISABLED)
        indicatormenu.add_command(label="None")
        indicatormenu.add_command(label="SMA", command=partial(AddIndicator,'sma','graph'))
        indicatormenu.add_command(label="EMA", command=partial(AddIndicator,'rsi','graph'))

        indicatormenu.add_command(label="----Bottom----", state=tk.DISABLED)
        indicatormenu.add_command(label="None")
        indicatormenu.add_command(label="RSI", command=partial(AddIndicator,'rsi','bottom'))
        indicatormenu.add_command(label="MACD", command=partial(AddIndicator,'macd','bottom'))

        tradingmenu = tk.Menu(self, tearoff=1)
        tradingmenu.add_command(label='Manual', command=partial(Popup, "Not yet implemented"))
        tradingmenu.add_command(label='Auto', command=partial(Popup, "Not yet implemented"))
        tradingmenu.add_separator()
        tradingmenu.add_command(label='Quick Buy', command=partial(Popup, "Not yet implemented"))
        tradingmenu.add_command(label='Quick Sell', command=partial(Popup, "Not yet implemented"))
        tradingmenu.add_command(label='Quick Trade Setup', command=partial(Popup, "Not yet implemented"))

        controlmenu = tk.Menu(self, tearoff=1)
        controlmenu.add_command(label='Start/Stop Stream', command=partial(Stream))
        controlmenu.add_command(label='Switch Scale', command=partial(Scale))
        controlmenu.add_command(label='Drawing Tools', command=partial(Popup, "Not yet implemented"))

        helpmenu = tk.Menu(self, tearoff=0)
        helpmenu.add_command(label='Tutorial', command=partial(Popup, "Not yet implemented"))
        helpmenu.add_command(label='Help', command=partial(Popup, "Not yet implemented"))
        helpmenu.add_command(label='About', command=partial(Popup, "Not yet implemented"))

        self.add_cascade(label="File", menu=filemenu)
        self.add_cascade(label="Exchange", menu=exchangemenu)
        self.add_cascade(label="Time Frame", menu=timeframemenu)
        self.add_cascade(label="Sample Size", menu=samplesizemenu)
        self.add_cascade(label="Indicators", menu=indicatormenu)
        self.add_cascade(label="Trading", menu=tradingmenu)
        self.add_cascade(label='Chart Control', menu=controlmenu)
        self.add_cascade(label='Help', menu=helpmenu)

class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        label = tk.Label(self,text="This app is in development and may or may not\n" +
                         "set your computer and all your life savings on fire.\n\n" +
                         "Do you recognize the risks and wish to continue?",font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self,text="Agree",
                            command=lambda: self.startup(controller))
        button1.pack()
        button2 = ttk.Button(self,text="Disagree",
                            command=Quit)
        button2.pack()
    def startup(self,controller,*args):
        Config('save')
        controller.show_frame(ButtonBar)
        controller.show_frame(GraphPage)

class GraphPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        w = ttk.Separator(self, orient=tk.VERTICAL)
        w.pack(side=tk.LEFT, fill=tk.Y)

        label = tk.Label(self,text="Graph",font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

class TradePage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        label = tk.Label(self,text="Trading Page",font=LARGE_FONT)
        label.grid(column=1,pady=10,padx=10)

        # Broken
        w = ttk.Separator(self, orient=tk.VERTICAL)
        w.grid(column=0, sticky="nsew")

class ButtonBar(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)


        label = tk.Label(self,text="Navigation",font=LARGE_FONT)
        label.pack()
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X)

        button1 = ttk.Button(self, text="Graph Page", command=lambda: controller.show_frame(GraphPage))
        button2 = ttk.Button(self, text="Trading Page", command=lambda: controller.show_frame(TradePage))

        button1.pack()
        button2.pack()

if __name__ == "__main__":
    app = TradeApp()
    app.geometry("1280x720")
    ani = animation.FuncAnimation(f, Animate, interval=5000)
    t = mp.Process(target=app.mainloop)
    t.start()
    t.join()
