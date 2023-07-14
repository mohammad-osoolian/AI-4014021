import gymnasium as gym
import numpy as np
from time import sleep

def round_method(num):
    return int(num*2)/2

def add_observation(rounded_obsrevs):
    if rounded_obsrevs in seen_observations:
        return 0
    seen_observations.append(rounded_obsrevs)
    return 1

best_action = {}
seen_observations = []
duplicates = 0
totalmoves = 0

env = gym.make("BipedalWalker-v3", hardcore=False, render_mode="human")
# Box2D
observation, info = env.reset(seed=42)
for _ in range(1000):
    action = env.action_space.sample()  # this is where you would insert your policy
    # action = np.array([0.0, 0.0, 0, -1])
    # print("action:", action) # back_hip front_hip back_knee front_knee  +1: pad sa'at gard  -1: sa'at gard
    observation, reward, terminated, truncated, info = env.step(action)
    # print("observations", observation)
    # print("reward", reward)
    rounded_obsrevs = [round_method(_) for _ in observation[:14]]
    if not add_observation(rounded_obsrevs):
        duplicates += 1
    if terminated or truncated:
        # observation, info = env.reset()
        break
    totalmoves+=1
    # sleep(0.25)
env.close()

print(duplicates, totalmoves)
