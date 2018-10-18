#!/usr/bin/Python3
import random

class grid:
    x_dim = 0 #X-Dimension of Grid
    y_dim = 0 #Y-Dimension of Grid
    ball_x = 0 #X Position of Ball
    ball_y = 0 #Y Position of Ball
    bx_initial = 0 #Remember initial ball x position for ball reset
    by_initial = 0 #Remember intial ball y position for ball reset
    goal_x = 0 #X position of Ball
    goal_y = 0 #Y Position of Ball
    min_dist = 0 #Minimum starting distance between ball and gol
    reward = 0 #Reward for ball reaching goal

    def set_ball_and_goal(self): #Assigns goal position and initial ball position
        self.ball_x = random.randint(1,(self.x_dim-2)) #Initialize ball away from a wall
        self.ball_y = random.randint(1,(self.x_dim-2))
        self.goal_x = random.randint(0,(self.x_dim-1)) #Goal can be along a wall
        self.goal_y = random.randint(0,(self.y_dim-1))
        dist = abs(self.goal_x - self.ball_x) + abs(self.goal_y - self.ball_y)

        while dist < self.min_dist: #Ball and goal must start a certain distance apart
            self.goal_x = random.randint(0, (self.x_dim - 1)) #Make sure grid is large enough to support min distance
            self.goal_y = random.randint(0, (self.y_dim - 1))
            self.ball_x = random.randint(1, (self.x_dim - 2))
            self.ball_y = random.randint(1, (self.x_dim - 2))
            dist = abs(self.goal_x - self.ball_x) + abs(self.goal_y - self.ball_y)
        self.bx_initial = self.ball_x
        self.by_initial = self.ball_y
        print('Ball Initial [X,Y]: ', [self.ball_x, self.ball_y])
        print('Goal [X,Y]: ', [self.goal_x, self.goal_y])

    def reset_ball(self): #Resets ball to initial position
        self.ball_x = self.bx_initial
        self.ball_y = self.by_initial
        print('Ball Initial [X,Y]: ', [self.ball_x, self.ball_y])

    def ball_react(self, action, agent_vec): #Utilized in agent_move function
        ax = agent_vec[0] #Agent X-Position
        ay = agent_vec[1] #Agent Y-Position
        if ax == self.ball_x and ay == self.ball_y: #Ball moves when agent occupies its state
            if action == 1: #Agent hit ball from the left
                self.ball_x += 1
                while self.ball_x > (self.x_dim-1): #Ball cannot be hit out of grid
                    self.ball_x -= 1
            if action == 2: #Agent hit ball from the right
                self.ball_x -= 1
                while self.ball_x < 0: #Ball cannot be hit out of grid
                    self.ball_x += 1
            if action == 3: #Agent hit ball from the bottom
                self.ball_y += 1
                while self.ball_y > (self.y_dim-1): #Ball cannot be hit out of grid
                    self.ball_y -= 1
            if action == 4: #Agent hit ball from the top
                self.ball_y -= 1
                while self.ball_y < 0: #Ball cannot be hit out of grid
                    self.ball_y += 1
            print('Ball Position: ', [self.ball_x, self.ball_y])

    def check_for_goal(self): #Check if ball is in goal
        if self.ball_x == self.goal_x and self.ball_y == self.goal_y:
            print('GOAL!!!')
            return self.reward #Return reward for getting ball in goal
        else:
            return 0


class agent:
    n_agents = 1 #Number of agents in the system
    agent_position = [] #Vector which tracks agent position in grid
    initial_position = [] #Remember starting positions of agents
    state_vec = [] #State vector

    def initialize_state_vec(self):
        self.state_vec = [0]*self.n_agents
        for i in range(self.n_agents):
            self.state_vec[i] = [0,0,0,0]

    def update_state_vec(self, gw): #gw is a "pointer" to grid class
        for i in range(self.n_agents):
            self.state_vec[i][0] = gw.ball_x - self.agent_position[i][0] #X distance from agent to ball
            self.state_vec[i][1] = gw.ball_y - self.agent_position[i][1] #Y distance from agent to ball
            self.state_vec[i][2] = gw.goal_x - gw.ball_x #X distance from ball to goal
            self.state_vec[i][3] = gw.goal_y - gw.ball_y #Y distance from ball to goal

    def set_agents(self, gw): #gw is "pointer" to grid class
        self.agent_position = [0]*self.n_agents
        self.initial_position = [0]*self.n_agents
        for i in range(self.n_agents):
            x = random.randint(0,(gw.x_dim-1))
            y = random.randint(0,(gw.y_dim-1))
            while x == gw.ball_x and y == gw.ball_y: #Agent cannot be initialized in same state as ball
                x = random.randint(0, (gw.x_dim - 1))
                y = random.randint(0, (gw.y_dim - 1))
            self.agent_position[i] = [x,y]
            self.initial_position[i] = [x,y]
        print('Agent Initial Position: ', self.agent_position)
        print(self.initial_position)

    def reset_agents(self): #Resets agents to starting position
        self.agent_position = self.initial_position
        print('Agent Initial Position: ', self.agent_position)
        print(self.initial_position)

    def agent_move(self, action, a_number, gw): #a_number identifies which agent is taking an action, gw is "pointer"
        x = self.agent_position[a_number][0]
        y = self.agent_position[a_number][1]
        if action == 1: #Agent moves right (positive x)
            x += 1
            while x > (gw.x_dim-1): #Prevent agent from moving outside grid
                x -= 1
        if action == 2: #Agent moves left (negative x)
            x -= 1
            while x < 0: #Prevent agent from moving outside grid
                x += 1
        if action == 3: #Agent moves up (positive y)
            y += 1
            while y > (gw.y_dim-1): #Prevent agent from moving outside grid
                y -= 1
        if action == 4: #Agent moves down (negative y)
            y -= 1
            while y < 0: #Prevent agent from moving outside grid
                y += 1
        self.agent_position[a_number][0] = x
        self.agent_position[a_number][1] = y
        print('Agent Position: ', self.agent_position[a_number])
        gw.ball_react(action, self.agent_position[a_number]) #Check if agent moved ball