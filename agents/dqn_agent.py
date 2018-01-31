import gym
import random
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, SimpleRNN, Flatten, Conv1D, MaxPooling1D
from keras.optimizers import Adam

# Deep Q-learning Agent
class DQNAgent:
    def __init__(self):
        self.memory = deque(maxlen=365)
        self.discount_rate = 0.95    # discount rate
        self.exploration_rate = 1  # exploration rate
        self.exploration_rate_min = 0.1
        self.exploration_rate_decay = 0.999
        self.learning_rate = 0.005
    def set_sizes(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
    def build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        # model.add(Conv1D(input_shape=(1,self.state_size),
        #          filters=self.state_size,
        #          kernel_size=1,
        #          activation='relu'))
        # model.add(MaxPooling1D(pool_size=1))
        # model.add(LSTM(128, activation='relu'))
        model.add(LSTM(128, input_shape=(1,self.state_size)))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(256, activation='sigmoid'))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        self.model = model
        return model
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    def act(self, state, random_act_values):
        if np.random.rand() <= self.exploration_rate:
            return random_act_values
        state = np.array(state).reshape((1,1,self.state_size))
        act_values = self.model.predict(state)
        return act_values[0]  # returns action
    def replay(self, batch_size):
        try: minibatch = random.sample(self.memory, batch_size)
        except: minibatch = self.memory
        for state, action, reward, next_state, done in minibatch:
            state = np.array(state).reshape((1,1,self.state_size))
            next_state = np.array(next_state).reshape((1,1,self.state_size))
            learned_value = reward
            if not done:
                learned_value = reward + self.discount_rate * self.model.predict(next_state)[0]
            target_f = (1 - self.learning_rate) * self.model.predict(state) + self.learning_rate * learned_value
            self.model.fit(state, target_f, epochs=12, verbose=0)
        if self.exploration_rate > self.exploration_rate_min:
            self.exploration_rate *= self.exploration_rate_decay
