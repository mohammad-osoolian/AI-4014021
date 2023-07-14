#actions :  back_hip front_hip back_knee front_knee  +1: pad sa'at gard  -1: sa'at gard

import gymnasium as gym
import numpy as np
from time import sleep
from utils import *
from features import feature_list

actionRange = (-1, +1)
alpha = 0.2
gamma = 0.95
epsilon = 0.2
stateStep = 0.001
actionStep = 0.25

def printStatus(s,a,samp):
    print(f's: {s} - a: {a}')
    print(f'sample: {samp}')
    print(f'Q(s,a): {Q.get((s,a), 0)}')
    print('--------------------------------------------------------')



f = feature_list
W = [1 for feat in f]
dis = Discretizer(stateStep, actionStep, actionRange)

AQL = ApproximateQLearning(alpha, gamma, epsilon, W, f, dis)


env = gym.make("BipedalWalker-v3", hardcore=False, render_mode='human')
observation, info = env.reset(seed=42)

tr = 0 
rn = 0
for _ in range(10000):
    # action = env.action_space.sample()
    s = AQL.extractState(observation)
    action = AQL.pickAction(s)
    a = AQL.extractAction(action)

    observation, reward, terminated, truncated, info = env.step(action)
    # print("action:", action)
    # print("observations", observation)
    # print("reward", reward)


    sp = AQL.extractState(observation)
    r = reward + sp[3]
    # if(sp[0]<-1 and sp[3]<0 and sp[2] > 0 and r>0):
    #     print('$$$$$$$$$$')
    #     r*=-1
    # if(sp[4] < sp[9]):
    #     r-=10
    print(AQL.updateW(s, a, r, sp), r)
    
    if terminated or truncated:
        observation, info = env.reset()
        # break
    # sleep(0.5)

env.close()