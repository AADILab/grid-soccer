#!/usr/bin/Python3
import random
import Grid_Soccer

def main():
    g = Grid_Soccer.grid(); a = Grid_Soccer.agent()

    g.x_dim = 5
    g.y_dim = 5
    g.min_dist = 2
    g.reward = 100
    a.n_agents = 1
    g.set_ball_and_goal()
    a.set_agents(g)

    print('\n') #Test Moving Ball in the X-Direction
    a.agent_position[0][0] = 0
    a.agent_position[0][1] = 0
    g.ball_x = 1
    g.ball_y = 0
    g.goal_x = 4
    g.goal_y = 0
    a.agent_move(1,0,g)
    rwd = g.check_for_goal()
    print('Reward = ', rwd)
    a.agent_move(1, 0, g)
    rwd = g.check_for_goal()
    print('Reward = ', rwd)
    a.agent_move(1, 0, g)
    rwd = g.check_for_goal()
    print('Reward = ', rwd)
    print('\n')

    g.reset_ball() #Test Ball Reset
    a.reset_agents() #Test Agent Reset

    print('\n') #Test ball moving in Y direction to goal
    a.agent_position[0][0] = 0
    a.agent_position[0][1] = 0
    g.ball_x = 0
    g.ball_y = 1
    g.goal_x = 0
    g.goal_y = 4
    a.agent_move(3, 0, g)
    rwd = g.check_for_goal()
    print('Reward = ', rwd)
    a.agent_move(3, 0, g)
    rwd = g.check_for_goal()
    print('Reward = ', rwd)
    a.agent_move(3, 0, g)
    rwd = g.check_for_goal()
    print('Reward = ', rwd)


main()