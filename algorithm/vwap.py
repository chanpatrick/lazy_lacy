import numpy as np
from numpy import genfromtxt
from collections import deque

class VWAP:
    def __init__(self):
        self.total_volume = 0
        self.total_value = 0
        self.vwap = 0
    def update(self, price, volume):
        if np.isnan(price): return self.vwap
        self.total_volume += volume
        self.total_value += volume * price
        self.vwap = self.total_value / self.total_volume
        return self.vwap

if __name__ == '__main__':
    data = genfromtxt('../data/AAPL.csv', delimiter=',', skip_header=1, usecols=range(1,7))
    prices = (data[:,1] + data[:,2] + data[:,3]) / 3
    volumes = data[:,5]
    prices = prices[:500]
    volumes = volumes[:500]
    vwap_curve = []
    vwap = VWAP()
    for i in range(len(prices)):
        vwap_curve.append(vwap.update(prices[i], volumes[i]))
        # raw_input("Press Enter to continue...")
    # print np.array(vwap_curve)
    import matplotlib.pyplot as plt
    x = range(len(prices))
    plt.plot(x, prices)
    plt.plot(x, vwap_curve)
    plt.show()
