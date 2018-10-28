from core import mod_utils as utils
import torch
import torch.nn as nn
import random
from torch.optim import Adam
from torch.autograd import Variable
import torch.nn.functional as F
from torch.nn import Parameter
import numpy as np


class SubPolicy(nn.Module):

    def __init__(self, state_dim, action_dim):
        super(SubPolicy, self).__init__()
        l1 = 128; l2 = 128; l3 = l2

        # Construct Hidden Layer 1
        self.w_l1 = nn.Linear(state_dim, l1)
        self.lnorm1 = nn.LayerNorm(l1)

        #Hidden Layer 2
        self.w_l2 = nn.Linear(l1, l2)
        self.lnorm2 = nn.LayerNorm(l2)


        #Out
        self.w_out = nn.Linear(l3, action_dim)


    def forward(self, input):

        #Hidden Layer 1
        out = self.w_l1(input)
        out = self.lnorm1(out)
        out = F.elu(out)

        #Hidden Layer 2
        out = self.w_l2(out)
        out = self.lnorm2(out)
        out = F.elu(out)


        #Out
        out = F.tanh(self.w_out(out))
        return out


class MasterPolicy(nn.Module):

    def __init__(self, state_dim, action_dim):
        super(MasterPolicy, self).__init__()
        l1 = 128; l2 = 128; l3 = l2

        # Construct Hidden Layer 1
        self.w_l1 = nn.Linear(state_dim, l1)
        self.lnorm1 = nn.LayerNorm(l1)

        #Hidden Layer 2
        self.w_l2 = nn.Linear(l1, l2)
        self.lnorm2 = nn.LayerNorm(l2)


        #Out
        self.w_out = nn.Linear(l3, action_dim)


    def forward(self, input):

        #Hidden Layer 1
        out = self.w_l1(input)
        out = self.lnorm1(out)
        out = F.elu(out)

        #Hidden Layer 2
        out = self.w_l2(out)
        out = self.lnorm2(out)
        out = F.elu(out)


        #Out
        out = self.w_out(out)
        return out


class Predilection(nn.Module):

    def __init__(self, state_dim, action_dim):
        super(Predilection, self).__init__()

        l1 = 200; l2 = 300; l3 = l2

        # Construct input interface (Hidden Layer 1)
        self.w_state1 = nn.Linear(state_dim, l1)
        self.w_action1 = nn.Linear(action_dim, l1)
        self.w_nextstate1 = nn.Linear(state_dim, l1)

        #Hidden Layer 1
        self.w_l1 = nn.Linear(3*l1, l2)
        self.lnorm1 = nn.LayerNorm(l2)

        #Out
        self.w_out = nn.Linear(l3, 1)
        self.w_out.weight.data.mul_(0.1)
        self.w_out.bias.data.mul_(0.1)



    def forward(self, state, nextstate, action):

        #Hidden Layer 1 (Input Interface)
        out_state = F.elu(self.w_state1(state))
        out_nextstate = F.elu(self.w_nextstate1(nextstate))
        out_action = F.elu(self.w_action1(action))
        out = torch.cat((out_state, out_nextstate, out_action), 1)

        # Hidden Layer 2
        out = self.w_l1(out)
        self.lnorm1(out)
        out = F.elu(out)

        # Output interface
        out = self.w_out(out)

        return out




class MetaAgent:
    def __init__(self, state_dim, action_dim, num_subpolicies, master_lr, sub_lr):
        self.state_dim = state_dim; self.action_dim = action_dim; self.num_subpolicies = num_subpolicies

        #Construct Master
        self.master = MasterPolicy(state_dim, num_subpolicies)

        #Construct the ensemble of sub-policies and predilections associated by list index
        self.subs = []; self.predilections = []
        for _ in range(num_subpolicies):
            self.subs.append(SubPolicy(state_dim, action_dim))
            self.predilections.append(Predilection(state_dim, action_dim))

        #Loss functions and optimizers
        self.master_loss = nn.MSELoss(); self.master_optim = Adam(self.master.parameters(), lr=master_lr)
        self.sub_loss = nn.MSELoss(); self.sub_optims = [Adam(self.subs[i].parameters(), lr=sub_lr) for i in range(num_subpolicies)]





    def act(self, state, epsilon=0.1):

        #Get Policy choice from the master
        master_action = torch.argmax(self.master.forward((state))).item()

        # Epsilon Greedy
        if random.random() < epsilon:
            master_action = random.randint(0, self.num_subpolicies-1)

        #Run selected sub to compute an action
        sub_action = torch.argmax(self.subs[master_action].forward(state)).item()

        return master_action, sub_action



    def learn_master(self, s, ma, ns, r, done, gamma, num_steps=1):

        for _ in range(num_steps):

            q = self.master.forward(s)[ma]
            with torch.no_grad():
                next_q = r + gamma * self.master.forward(ns)[ma] * (1 - done)

            self.master_optim.zero_grad()
            dt = self.master_loss(next_q, q)
            dt.backward()
            self.master_optim.step()


    def learn_sub(self, s, a, ns, gamma, num_steps=1):

        for _ in range(num_steps):

            for predilection, sub_optim in zip(self.predilections, self.sub_optims):
                sub_optim.zero_grad()
                policy_loss = -predilection.forward(s, ns, a).sum()
                policy_loss.backward()
                sub_optim.step()






















