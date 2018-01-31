import numpy as np
from numpy import genfromtxt
from collections import deque

class RSI:
    def __init__(self,period=14):
        self.period = period
        self.gains = deque(maxlen=period)
        self.losses = deque(maxlen=period)
        self.prices = deque(maxlen=period)
        self.avg_gain = None
        self.avg_loss = None
        self.rsi = 50
    def update(self, price, smooth=False):
        if np.isnan(price):
            return self.rsi
        self.prices.append(price)
        if len(self.prices) >= self.period:
            # Calculate unreadlized gain and loss
            avg_price_per_period = np.mean(self.prices)
            unrealized = (price - avg_price_per_period) / avg_price_per_period
            gain = unrealized if unrealized > 0 else 0
            loss = -unrealized if unrealized < 0 else 0
            self.gains.append(gain)
            self.losses.append(loss)
            if len(self.gains) != self.period:
                self.rsi = 50
            else:
                # Set initial
                if self.avg_gain == None or smooth == False:
                    self.avg_gain = np.mean(self.gains)
                    self.avg_loss = np.mean(self.losses)
                else:
                    # smoothing
                    self.avg_gain = (self.avg_gain * (self.period - 1) + np.mean(self.gains)) / self.period
                    self.avg_loss = (self.avg_loss * (self.period - 1) + np.mean(self.losses)) / self.period
                self.rsi = 100 - 100 / (1 + self.avg_gain / self.avg_loss)
        return self.rsi

if __name__ == '__main__':
    data = genfromtxt('../data/AAPL.csv', delimiter=',', skip_header=1, usecols=range(1,7))
    prices = (data[:,1] + data[:,2] + data[:,3]) / 3
    rsi_curve = []
    rsi = RSI(period=14)
    prices = prices[:500]
    for i in range(len(prices)):
        # purchase = i in [20,100,256,747]
        # purchase = i in [14]
        rsi_curve.append(rsi.update({'Price':prices[i]},smooth=True))
        # raw_input("Press Enter to continue...")
    # print np.array(rsi_curve)
    import matplotlib.pyplot as plt
    x = range(len(prices))
    plt.plot(x, rsi_curve)
    plt.show()
