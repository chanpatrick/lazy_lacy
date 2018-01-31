import numpy as np
from numpy import genfromtxt
from collections import deque

class Volatility:
    def __init__(self, period=10):
        self.period = period
        self.prices = deque(maxlen=period)
        self.prev_volitility = None
        self.volitility = None
    def update(self, price):
        if np.isnan(price):
            return self.volitility if self.volitility != None else 0
        self.prices.append(price)
        self.volitility = np.std(self.prices)
        return self.volitility
