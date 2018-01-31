import numpy as np
from numpy import genfromtxt
from collections import deque

class EMA:
    def __init__(self, period=10):
        self.period = period
        self.prices = deque(maxlen=period)
        self.prev_ema = None
        self.ema = None
        self.multiplier = (2. / (self.period + 1))
    def update(self, price):
        if np.isnan(price):
            return self.ema if self.ema != None else price
        self.prices.append(price)
        if len(self.prices) >= self.period:
            # Set initial ema
            if self.prev_ema == None: self.prev_ema = price
            # Calculate new ema value from current price
            new_ema = (price - self.prev_ema) * self.multiplier + self.prev_ema
            # Update the new ema value
            if self.ema == None: self.ema = new_ema
            else:
                self.prev_ema = self.ema
                self.ema = new_ema
        if self.ema == None: return price
        else: return self.ema
    def initial_sma(self):
        return self.period - np.sum(self.prices) / self.period

if __name__ == '__main__':
    data = genfromtxt('../data/AAPL.csv', delimiter=',', skip_header=1, usecols=range(1,7))
    prices = (data[:,1] + data[:,2] + data[:,3]) / 3
    prices = prices[:500]
    ema_curve = []
    ema = EMA(period=15)
    for p in prices:
        ema_curve.append(ema.update(p))
        # raw_input("Press Enter to continue...")
    print np.array(ema_curve)
    import matplotlib.pyplot as plt
    x = range(len(prices))
    plt.plot(x, prices)
    plt.plot(x, ema_curve)
    plt.show()
