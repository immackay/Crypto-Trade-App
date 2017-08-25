import pandas as pd
import numpy as np
import urllib, json

class bitfinex:
    resturl = 'https://api.bitfinex.com/v2/'
    def __init__(self, APIKey, Secret):
        self.APIKey = APIKey
        self.Secret = Secret

    def api_query(self, command, req={}):
        return

    def returnTicker()
