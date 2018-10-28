#!/usr/bin/Python3
import random

class grid(object):
    def __init__(self, x_dim=10, y_dim=10, min_dist=2, reward=100):
        """
        Params:
            x_dim: x dimension of the world
            y_dim: y dimension of the world
            min_dist: minimum distance between ball and goal at the start 
            reward: what reward to hand out when goal condition is reached.
        """
        self.x_dim = x_dim #X-Dimension of Grid
        self.y_dim = y_dim #Y-Dimension of Grid
        self.ball_x = 0 #X Position of Ball
        self.ball_y = 0 #Y Position of Ball
        self.bx_initial = 0 #Remember initial ball x position for ball reset
        self.by_initial = 0 #Remember intial ball y position for ball reset
        self.goal_x = 0 #X position of Ball
        self.goal_y = 0 #Y Position of Ball
        self.min_dist = min_dist #Minimum starting distance between ball and gol
        self.reward = reward #Reward for ball reaching goal

        #Assigns goal position and initial ball position
        self.ball_x = random.randint(1,self.x_dim-2) # Start at 1 to initialize ball away from a wall
        self.ball_y = random.randint(1,self.x_dim-2)
        self.goal_x = random.randint(0,self.x_dim-1) #Goal can be along a wall
        self.goal_y = random.randint(0,self.y_dim-1)
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


class agent(object):
    def __init__(self, gw):
        """
        Params:
            gw: the world object, needed to get some of the dimensions and numbers right
        """
        self.n_agents = 1 #Number of agents in the system
        self.agent_position = [] #Vector which tracks agent position in grid
        self.initial_position = [] #Remember starting positions of agents
        self.state_vec = [] #State vector

        self.state_vec = [0]*self.n_agents
        for i in range(self.n_agents):
            self.state_vec[i] = [0,0,0,0]

        # Set initial position
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

    def update_state_vec(self, gw): #gw is a "pointer" to grid class
        """ DEPRECATED """
        for i in range(self.n_agents):
            self.state_vec[i][0] = gw.ball_x - self.agent_position[i][0] #X distance from agent to ball
            self.state_vec[i][1] = gw.ball_y - self.agent_position[i][1] #Y distance from agent to ball
            self.state_vec[i][2] = gw.goal_x - gw.ball_x #X distance from ball to goal
            self.state_vec[i][3] = gw.goal_y - gw.ball_y #Y distance from ball to goal

    def reset_agents(self): #Resets agents to starting position
        self.agent_position = self.initial_position
        print('Agent Initial Position: ', self.agent_position)
        print(self.initial_position)

    def agent_move(self, action, a_number, gw): #a_number identifies which agent is taking an action, gw is "pointer"
        """
        Moves the agent in the world.

        Params:
            action: integer in [1,4], where they are equate to 
                1: right
                2: left
                3: up
                4: down
            a_number: identifies the agent being moved
            gw: grid world object reference

        Returns: None

        Postconditions:
            self._agent_position is updated with the position,
            after action and world effects are taken into account.
        """
                
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

class GridBallWorld(object):
    """
    OpenAI Gym style interface for the ball-pushing domain.
    Single-agent problem by default.
    """
    def __init__(self, x_dim=10, y_dim=10, min_dist=2, reward=100):
        self._world = grid(x_dim, y_dim, min_dist, reward)
        self._agent = agent(self._world)

    def _get_state(self):
        """ Helper to get the state of the world. """
        state = []
        a_x , a_y= self._agent.agent_position[0][0], self._agent.agent_position[0][1]
        # Relative ball pos
        state.append(a_x - self._world.ball_x)
        state.append(a_y - self._world.ball_y)
        # Relative goal pos
        state.append(a_x - self._world.goal_x)
        state.append(a_y - self._world.goal_y)
        # Relative wall distances
        state.append(a_x)
        state.append(self._world.x_dim-1 - a_x)
        state.append(a_y)
        state.append(self._world.y_dim-1 - a_y)

        return state

    def reset(self):
        self._world.reset_ball()
        self._agent.reset_agents()

    def step(self, action):
        """
        Steps the world 1 timestep.

        Params:
            action: integer in [1,4], where they are equate to 
                1: right
                2: left
                3: up
                4: down
        Returns:
            State: the updated state of the world after action a
            Reward: float, the current reward
            Done: boolean flag
            Info: dict, empty
        """
        self._agent.agent_move(action, 0, self._world)
        state = self._get_state()
        reward = self._world.check_for_goal()
        if reward > 0:
            done = True
        else:
            done = False
        info = {}
        return state, reward, done, info



