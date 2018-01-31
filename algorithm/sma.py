import numpy as np
from numpy import genfromtxt
from collections import deque

class SMA:
    def __init__(self, period=10):
        self.period = period
        self.prices = deque(maxlen=period)
        self.sma = None
    def update(self, price):
        if np.isnan(price):
            return self.sma if self.sma != None else price
        self.prices.append(price)
        if len(self.prices) == self.period:
            self.sma = np.sum(self.prices) / self.period
        if self.sma == None: return price
        else: return self.sma

if __name__ == '__main__':
    data = genfromtxt('../data/AAPL.csv', delimiter=',', skip_header=1, usecols=range(1,7))
    prices = (data[:,1] + data[:,2] + data[:,3]) / 3
    prices = prices[:500]
    sma_curve = []
    sma = SMA(period=10)
    for p in prices:
        sma_curve.append(sma.update(p))
        # raw_input("Press Enter to continue...")
    # print np.array(sma_curve)
    import matplotlib.pyplot as plt
    x = range(len(prices))
    plt.plot(x, prices)
    plt.plot(x, sma_curve)
    plt.show()
