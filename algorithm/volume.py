import numpy as np
from numpy import genfromtxt
from collections import deque

class Volume:
    def __init__(self, period=14):
        self.period = period
        self.volume = 0
    def update(self, volume):
        if np.isnan(volume): return self.volume
        self.volume = (self.volume * (self.period-1) - volume) / self.period
        return self.volume
