import numpy as np
import matplotlib.pyplot as plt
from collections import deque
np.set_printoptions(precision=4)

from lazy_lacy.agents.dqn_agent import DQNAgent
from lazy_lacy.market.stock import Stock

if __name__ == '__main__':
    action_size = 1 # signed int to determine percentage trade amount
    episodes = 100000
    max_days = 30
    max_day_held = 30
    max_performance = 0

    agent = DQNAgent()

    # Setup stocks
    stocks = [
        Stock('../data/AAPL.csv'),
        Stock('../data/MSFT.csv'),
        Stock('../data/^GSPC.csv')
    ]
    agent.set_sizes(
        state_size=len(stocks)*len(stocks[0].analyze_data(stocks[0].data[0])),#+1,
        action_size=len(stocks)
    )
    agent.build_model()
    plt_array = []
    plt.ion()

    for e in range(episodes):
        initial_capital = 5000
        cash = initial_capital
        start_idx = np.random.randint(int(len(stocks[0].data))-365*3,int(len(stocks[0].data)))
        end_idx = int(len(stocks[0].data))
        high = 0
        low = None
        stop_idx = 0
        done = False
        state = np.array([stock.analyze_data(stock.data[start_idx]) for stock in stocks]).flatten()
        # state = np.append(state, 0)
        reward = 0
        for idx in range(start_idx+1,end_idx):
            action = agent.act(state, random_act_values=[np.random.uniform(-1.0,1.0) for i in range(len(stocks))])
            next_state = np.array([stock.analyze_data(stock.data[idx]) for stock in stocks]).flatten()
            for stock_idx, allocation in enumerate(action):
                stock = stocks[stock_idx]
                price = stock.data[idx]['Price']
                if price > high:
                    high = low = price
                if price < low:
                    low = price
                cash, partial_reward = stock.trade(
                    cash=cash,
                    allocation=allocation,
                    price_now=price,
                    trading_fee=5,
                    trade=True
                )
                reward += partial_reward
                if partial_reward != 0: reward += 0.5 # reward for executing a trade
            reward += 0.5 # reward for not giving up
            # next_state = np.append(next_state, reward)
            stop_idx = idx
            next_state = np.reshape(next_state, [1, agent.state_size])
            done = all([stock.days_held > max_day_held for stock in stocks])# or idx-start_idx+1 > max_days
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                break
        performance = int(30.0*(np.sum([stock.notional_value for stock in stocks])-initial_capital)/(stop_idx-start_idx))
        max_performance = performance if performance > max_performance else max_performance
        try:
            val = np.sum([stock.notional_value for stock in stocks])
            plt.scatter(e, val)
            plt.ylim(ymin=0,ymax=initial_capital*2)
            plt.pause(0.05)
            print 'E[{}/{}] ({}):\ttotal=${}\tincome=${}/month\tmax=${}/month\ttimes_traded={}\t'.format(e,episodes,\
                stop_idx-start_idx, \
                # [stock.position for stock in stocks])
                cash + np.sum([stock.notional_value for stock in stocks]), \
                performance, max_performance, \
                int(np.sum([stock.times_traded for stock in stocks])), \
            )
        except:
            pass
        max_day_held = max([int(max_performance/3),30])
        for stock in stocks:
            stock.reset()
        agent.replay(32)

while True:
    plt.pause(0.05)
