from numpy import genfromtxt

def load_yahoo_finance_csv(fname, start=None, end=None):
    data = genfromtxt('../data/AAPL.csv', delimiter=',', skip_header=1, usecols=range(1,7))
    out = []
    for d in data:
        out.append({
            'Open': d[0],
            'High': d[1],
            'Low': d[2],
            'Close': d[3],
            'Adj Close': d[4],
            'Volume': d[5],
            'Price': (d[3]+d[1]+d[2])/3.0
        })
    return out
