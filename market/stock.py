from lazy_lacy.algorithm.bollinger_band import BollingerBand
from lazy_lacy.algorithm.candle_stick import CandleStick
from lazy_lacy.algorithm.ema import EMA
from lazy_lacy.algorithm.sma import SMA
from lazy_lacy.algorithm.rsi import RSI
from lazy_lacy.algorithm.vwap import VWAP
from lazy_lacy.algorithm.volatility import Volatility
from lazy_lacy.algorithm.volume import Volume
from lazy_lacy.market.data import load_yahoo_finance_csv
import numpy as np
import os
from collections import deque

class Stock:
    def __init__(self, fname):
        self.technical_indicators = [
            Volatility(period=12),
            Volatility(period=96),
            Volatility(period=672),
            CandleStick(period=14),
            EMA(period=21),
            EMA(period=55),
            EMA(period=89),
            RSI(period=14),
            RSI(period=32),
            RSI(period=61),
            Volume(period=12),
            Volume(period=34),
            Volume(period=96),
            SMA(period=9),
            SMA(period=14),
            SMA(period=60)
        ]
        self.name = os.path.basename(fname)
        self.position = 0
        self.price_bought = 0
        self.days_held = 0
        self.notional_value = 0
        self.times_traded = 0
        self.data = load_yahoo_finance_csv(fname)
    def reset(self):
        self.position = 0
        self.price_bought = 0
        self.days_held = 0
        self.times_traded = 0
        self.notional_value = 0
    def analyze_data(self, d):
        data = []
        for ti in self.technical_indicators:
            class_name = ti.__class__.__name__
            if class_name in ['VWAP']:
                output = ti.update(d['Price'],d['Volume'])
            elif class_name in ['CandleStick']:
                output = ti.update(d['Price'],d['Open'],d['Close'],d['High'],d['Low'])
            else:
                output = ti.update(d['Price'])
            if isinstance(output, (list, tuple)):
                data += output
            else:
                data.append(output)
        data += d.values()
        return data
    def trade(self, cash, allocation, price_now, trade=True, trading_fee=5):
        if np.isnan(price_now) or allocation == 0 or trade == False:
            self.days_held += 1
            return cash, 0
        shares = int(allocation*cash/price_now)
        if self.position + shares < 0:
            self.days_held += 1
            return cash, 0
        if not self.price_bought: self.price_bought = price_now
        gain = price_now*shares
        cost = self.price_bought*shares + trading_fee
        roi = (gain-cost)/cost
        if cash > cost:
            self.position += shares
            self.price_bought = price_now
            self.days_held = 1
            self.times_traded += 1
            self.notional_value = self.position * price_now
            return cash - cost, roi
        else:
            self.days_held += 1
            return cash, 0
