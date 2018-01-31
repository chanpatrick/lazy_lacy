import numpy as np
from numpy import genfromtxt
from collections import deque

class BollingerBand:
    def __init__(self, period=10):
        self.period = period
        self.prices = deque(maxlen=period)
        self.high_band = None
        self.mid_band = None
        self.low_band = None
        self.std = None
    def update_for_visual(self, price):
        if np.isnan(price):
            return self.get_bands_for_visual()
        self.prices.append(price)
        if len(self.prices) >= self.period:
            sma = np.sum(self.prices) / self.period
            std = np.std(self.prices)
            self.high_band = sma + std*2
            self.mid_band = sma
            self.low_band = sma - std*2
        return self.get_bands_for_visual(price)
    def update(self, price):
        if np.isnan(price):
            return self.get_bands()
        self.prices.append(price)
        if len(self.prices) >= self.period:
            sma = np.sum(self.prices) / self.period
            std = np.std(self.prices)
            self.mid_band = sma
            self.std = std
        return self.get_bands(price)
    def get_bands_for_visual(self,price=None):
        if self.low_band == None and price != None:
            return [price, price, price]
        return [self.low_band, self.mid_band, self.high_band]
    def get_bands(self, price=None):
        if self.mid_band == None and price != None:
            return [price, np.std(self.prices)]
        return [self.mid_band, self.std]

if __name__ == '__main__':
    data = genfromtxt('../data/AAPL.csv', delimiter=',', skip_header=1, usecols=range(1,7))
    prices = (data[:,1] + data[:,2] + data[:,3]) / 3
    prices = prices[:1000]
    low = []
    mid = []
    high = []
    std = []
    bb = BollingerBand(period=20)
    for p in prices:

        # lmh = bb.update(p)
        # low.append(lmh[0])
        # mid.append(lmh[1])
        # high.append(lmh[2])


        ms = bb.update_for_model(p)
        mid.append(ms[0])
        std.append(ms[1])

        # raw_input("Press Enter to continue...")
    import matplotlib.pyplot as plt
    x = range(len(prices))
    # plt.plot(x, prices)
    # plt.plot(x, low)
    plt.plot(x, mid)
    # plt.plot(x, high)
    plt.plot(x, std)
    plt.show()
