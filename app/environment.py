import numpy as np

class SimpleEnvironment:
    def reset(self):
        return [0]

    def step(self, action):
        next_state = [np.random.choice([0, 1])]
        reward = np.random.choice([0, 1])
        done = np.random.choice([True, False])
        return next_state, reward, done
