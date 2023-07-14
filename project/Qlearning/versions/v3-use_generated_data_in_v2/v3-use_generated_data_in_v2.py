import gymnasium as gym
import numpy as np
from time import sleep
from utils import *

actionRange = (-1, +1)
td = TrainedData()


def makeActionSpace():
    actionSpace = []
    actionRng = dis.discreteActionRange()
    for joint1 in actionRng:
        for joint2 in actionRng:
            for joint3 in actionRng:
                for joint4 in actionRng:
                    actionSpace.append((joint1, joint2, joint3, joint4))
    return actionSpace

def sample(r, sp):
    maxQ = 0
    for ap in makeActionSpace():
        maxQ = max(maxQ, gamma * Q.get((sp,ap), 0))
    return r + maxQ

def optimalAction(s):
    actionSpace = makeActionSpace()
    optact = actionSpace[-1]
    maxQ = Q.get((s,optact), 0)
    for a in actionSpace:
        if Q.get((s,a), 0) > maxQ:
            maxQ = Q.get((s,a), 0)
            optact = a
    return optact


def printStatus(s,a,samp):
    print(f's: {s} - a: {a}')
    print(f'sample: {samp}')
    print(f'Q(s,a): {Q.get((s,a), 0)}')
    print('--------------------------------------------------------')

Q = {}
Q = td.readData()
alpha = 0.2
gamma = 1
dis = Discretizer(1, .5, actionRange)

env = gym.make("BipedalWalker-v3", hardcore=False, render_mode='human')
# Box2D
observation, info = env.reset(seed=42)

for _ in range(10000):
    # action = env.action_space.sample()
    s = tuple(dis.roundState(observation)[:14])
    action = optimalAction(s)
    print(action)
    a = tuple(dis.roundAction(action))

    observation, reward, terminated, truncated, info = env.step(action)
    # print("action:", action) # back_hip front_hip back_knee front_knee  +1: pad sa'at gard  -1: sa'at gard
    # print("observations", observation)
    # print("reward", reward)


    sp = tuple(dis.roundState(observation)[:14])
    r = reward
    samp = sample(r, sp)
    print(f'Q(s,a): {Q.get((s,a), 0)}')
    Q[(s,a)] = (1-alpha)*Q.get((s,a), 0) + alpha*samp
    printStatus(s, a, samp)
    
    if terminated or truncated:
        observation, info = env.reset()
        # break
    # sleep(1)

env.close()

# td.writeData(Q)