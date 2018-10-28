#!/usr/bin/Python3
import random
import Grid_Soccer
import numpy as np, os, random

from core import mod_utils as utils
import  torch
from core import replay_memory
import argparse
from core import metagent as magent


SEED = 7


class Parameters:
    def __init__(self):

        self.num_subs = 5

        #Policy Gradient
        self.master_gamma = 0.99
        self.sub_gamma = 0.99
        self.master_lr = 1e-3
        self.sub_lr = 1e-2
        self.batch_size = 128
        self.buffer_size = 1000000
        self.num_gradient_steps = 4

        #Save Results
        self.state_dim = 8; self.action_dim = 4
        self.save_foldername = 'R_Meta/'
        if not os.path.exists(self.save_foldername): os.makedirs(self.save_foldername)

class Learner:
    def __init__(self, args, env):
        self.args = args; self.env = env

        #Create the Agent
        self.agent = magent.MetaAgent(args.state_dim, args.action_dim, args.num_subs, args.master_lr, args.sub_lr)

        #Init Replay Buffer
        self.replay_buffer = replay_memory.ReplayMemory(args.buffer_size)


    def add_experience(self, s, a, ns):
        onehot_a = np.zeros((self.args.action_dim))
        onehot_a[a-1] = 1
        a = utils.to_tensor(onehot_a).unsqueeze(0)
        self.replay_buffer.push(s, a, ns)


    def evaluate(self, agent, master_epsilon, sub_epsilon):

        total_reward = 0.0
        s = self.env.reset()
        s = utils.to_tensor(s).unsqueeze(0)
        done = False

        ms = []; ma = []; mns = []; mr = []; mdone = []

        while not done:

            #Take action
            master_action, sub_action = agent.act(s, master_epsilon)

            #Sample sub-action from sub-action dist
            if random.random() < sub_epsilon:
                sub_action = random.randint(0, self.args.action_dim)

            # Simulate one step in environment
            ns, r, done, info = self.env.step(sub_action+1)

            ns = utils.to_tensor(ns).unsqueeze(0)
            total_reward += r

            #Add to replay buffer
            self.add_experience(s, sub_action, ns)

            #Add to master buffer (temporary)
            ms.append(s); ma.append(utils.to_tensor(np.array([master_action])).unsqueeze(0).long()); mns.append(ns); mr.append(utils.to_tensor(np.array([r])).unsqueeze(0)); mdone.append(utils.to_tensor(np.array([float(done)])).unsqueeze(0))

            s = ns


        return total_reward, torch.cat(ms), torch.cat(ma), torch.cat(mns), torch.cat(mr), torch.cat(mdone)



    def train(self):



        ####################### PG #########################
        #Collect experience
        score, ms, ma, mns, mr, mdone = self.evaluate(self.agent, master_epsilon=0.1, sub_epsilon=0.1) #Train

        #On-PG in master
        self.agent.learn_master(ms, ma, mns, mr, mdone, self.args.master_gamma, self.args.num_gradient_steps)

        #Off-PG for Subs
        if len(self.replay_buffer) > self.args.batch_size * 5:
            transitions = self.replay_buffer.sample(self.args.batch_size)
            batch = replay_memory.Transition(*zip(*transitions))
            self.agent.learn_sub(torch.cat(batch.state), torch.cat(batch.action), torch.cat(batch.next_state), self.args.sub_gamma, self.args.num_gradient_steps)

        return score





if __name__ == "__main__":
    parameters = Parameters()  # Create the Parameters class
    tracker = utils.Tracker(parameters, ['sokoban'], '_score.csv')  # Initiate tracker


    #Create Env
    env = Grid_Soccer.GridBallWorld()

    #Seed
    torch.manual_seed(SEED); np.random.seed(SEED); random.seed(SEED)

    #Create Agent
    learner = Learner(parameters, env)



    for gen in range(1000000):
        score = learner.train()
        print('#Gen:', gen, ' Score:', '%.2f'%score, 'Buffer_Size', learner.replay_buffer.__len__() )
        print()
        tracker.update([score], gen)













