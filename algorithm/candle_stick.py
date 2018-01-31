import numpy as np
from numpy import genfromtxt
from collections import deque

class CandleStick:
    def __init__(self,period=14):
        # The coordinate represent relative position and height of candle sticks
        self.period = period
        self.lh = deque(maxlen=period)
        self.oc = deque(maxlen=period)
        self.oh = deque(maxlen=period)
        self.cl = deque(maxlen=period)
        self.ol = deque(maxlen=period)
        self.ch = deque(maxlen=period)
    def update(self, price, open, close, high, low):
        if np.isnan(price):
            return np.mean(self.lh), np.mean(self.oc), np.mean(self.oh), np.mean(self.cl), np.mean(self.ol), np.mean(self.ch)
        self.lh.append(low-high)
        self.oc.append(open-close)
        self.oh.append(open-low)
        self.cl.append(close-high)
        self.ol.append(open-high)
        self.ch.append(close-low)
        return np.mean(self.lh), np.mean(self.oc), np.mean(self.oh), np.mean(self.cl), np.mean(self.ol), np.mean(self.ch)

if __name__ == '__main__':
    data = genfromtxt('../data/AAPL.csv', delimiter=',', skip_header=1, usecols=range(1,7))
    prices = (data[:,1] + data[:,2] + data[:,3]) / 3
    start = 0
    end = 2000
    prices = prices[start:end]
    open = data[:,0][start:end]
    high = data[:,1][start:end]
    low = data[:,2][start:end]
    close = data[:,3][start:end]
    lh_curve = []
    oc_curve = []
    oh_curve = []
    cl_curve = []
    ol_curve = []
    ch_curve = []
    cs = CandleStick()
    for i in range(len(prices)):
        lh, oc, oh, cl, ol, ch = cs.update(prices[i],open[i],close[i],high[i],low[i])
        lh_curve.append(lh)
        oc_curve.append(oc)
        oh_curve.append(oh)
        cl_curve.append(cl)
        ol_curve.append(ol)
        ch_curve.append(ch)
        # raw_input("Press Enter to continue...")
    # print np.array(inner_candle_stick)
    import matplotlib.pyplot as plt
    x = range(len(prices))
    plt.plot(x, prices)
    plt.plot(x, np.array(lh_curve))
    plt.plot(x, np.array(oc_curve))
    plt.plot(x, np.array(oh_curve))
    plt.plot(x, np.array(cl_curve))
    plt.plot(x, np.array(ol_curve))
    plt.plot(x, np.array(ch_curve))
    plt.show()
