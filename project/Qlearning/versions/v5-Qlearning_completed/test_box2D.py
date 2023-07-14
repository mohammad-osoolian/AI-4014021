#actions :  back_hip front_hip back_knee front_knee  +1: pad sa'at gard  -1: sa'at gard

import gymnasium as gym
import numpy as np
from time import sleep
from utils import *

actionRange = (-1, +1)
alpha = 0.2
gamma = 0.9
epsilon = 1
stateStep = 1
actionStep = 0.5
td = TrainedData()

def printStatus(s,a,samp):
    print(f's: {s} - a: {a}')
    print(f'sample: {samp}')
    print(f'Q(s,a): {Q.get((s,a), 0)}')
    print('--------------------------------------------------------')



Q = td.readData()
dis = Discretizer(stateStep, actionStep, actionRange)

QL = QLearning(alpha, gamma, epsilon, Q, dis)



env = gym.make("BipedalWalker-v3", hardcore=False, render_mode='human')
observation, info = env.reset(seed=42)

for _ in range(10000):
    # action = env.action_space.sample()
    s = QL.extractState(observation)
    action = QL.pickAction(s)
    a = QL.extractAction(action)

    observation, reward, terminated, truncated, info = env.step(action)
    # print("action:", action)
    # print("observations", observation)
    # print("reward", reward)


    sp = QL.extractState(observation)
    r = reward
    QL.updateQ(s, a, r, sp)
    QL.epsilon*=0.9997
    print(QL.epsilon)
    
    if terminated or truncated:
        observation, info = env.reset()
        # break
    # sleep(1)

env.close()
td.writeData(Q)