#!/usr/bin/Python3
import random
import Grid_Soccer

env = Grid_Soccer.GridBallWorld()

env.reset()
s, r, d, i = env.step(1)
