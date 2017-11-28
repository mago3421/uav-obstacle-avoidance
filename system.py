"""
Name: System class
Project: UAV Obstacle Avoidance Using Q-Learning Techniques
Authors: Katherine Glasheen, Marc Gonzalez, Shayon Gupta,
Travis Hainsworth, Ramya Kanlapuli

Description: This class serves as the driver for running the
system simulation including training and testing the agent's model
"""

import pickle
import os
from visualizer import *
from entity import *
from uav import *
from agent import *
from game_data import *
from environment import *
from Q_matrix import *
from numpy import random


class system:
    # Function to initialize system
    def __init__(self, grid_file, modelType = "Standard"):
        self.grid_file = grid_file
        # initialize modelType
        self.modelType = modelType
        # initialize Q matrix for standard learning
        #self.Q = None
        # Set simulation entities to initial conditions from file
        self.reset(self.grid_file)
        # Set simulation state to running
        self.running = True
        self.qObj = []
        if os.path.isfile('./q_dump.pickle'):
            self.qObj.load_Q()
        else:
            self.qObj.reset_Q()

    # Function to reset the state of the system from input file
    def reset(self, grid_file=None, random_agent_start = False):
        # Set file the system uses to reset itself
        self.grid_file = grid_file if grid_file else self.grid_file
        # Initialize dictionary of entities
        self.entities = {"agent": None,
                         "uav": [],
                         "goal": None,
                         "entity": []}
        # Open grid file to initialize dimension and objects
        with open(self.grid_file, 'r') as f:
            # Initialize square dimension of grid
            self.dim = int(f.readline().strip('\n'))
            # Initialize objects
            for line in f:
                object_type, row, col = (line.strip('\n')).split(' ')
                row = int(row)
                col = int(col)
                if object_type == "agent":
                    self.entities["agent"] = agent([row, col], self.modelType)
                elif object_type == "goal":
                    self.entities["goal"] = entity([row, col])
                elif object_type == "uav":
                    self.entities["uav"].append(uav([row, col]))
                elif object_type == "entity":
                    self.entities["entity"].append(entity([row, col]))
		# If requested randomize the agent's location
        if random_agent_start == True:
            x_rand = round(random.random()*self.dim)
            y_rand = round(random.random()*self.dim)
            self.entities["agent"].location[0] = x_rand
            self.entities["agent"].location[0] = y_rand
        # reset the running boolean
        self.running = True
        # initialize the object for the Q-matrix
        self.qObj = Q_matrix(self.dim)

    # Function to load new grid file for use in self.reset(f)
    def load_file(self, grid_file):
        # Set grid file
        self.grid_file = grid_file
        # Initialize system based on new file
        self.reset(self.grid_file)

    # Function which evolves the system by one timestep
    def step(self):
        # Move dynamic obstacles
        for uav in self.entities["uav"]: uav.move()
        # Move agent
        self.entities["agent"].move(self.qObj)
        # Perform collision detection
        self.detect_collisions()
        # Check if UAV made it to goal or crashed
        if (self.entities["agent"].get_location() == self.entities["goal"].get_location()) or self.entities[
            "agent"].check_crash():
            # Halt system because of crash or goal reached
            self.running = False
        # If simulation is still running
        else:
            # Update agent rewards
            self.update_rewards()

    # Function which that wraps the agent observe function and feeds the agent its horizon at the end of each round
    def update_rewards(self):
        # Construct dictionary to feed agent its rewards
        empty = self.entities["agent"].rewards["empty"]
        rewards = {"up": empty, "down": empty, "left": empty, "right": empty}
        offsets = {"up": [0, 1], "down": [0, -1], "left": [-1, 0], "right": [1, 0]}
        # Check locations around agent
        agent_loc = self.entities["agent"].get_location()
        # Check all rewards against system bounds and object locations
        for reward in rewards.keys():
            # Set offset location w.r.t. agent location and offset
            reward_loc = [agent_loc + offset for agent_loc, offset in zip(agent_loc, offsets[reward])]
            # horizon_loc = [agent_loc + (2 * offset) foragent_loc, offset in zip(agent_loc, offsets[reward])]
            # First check if reward is out bounds
            if reward_loc[0] < 0 or reward_loc[0] >= self.dim or reward_loc[1] < 0 or reward_loc[1] >= self.dim:
                # Set reward and continue in loop
                rewards[reward] = self.entities["agent"].rewards["oob"]
                continue
            else:
                # Get distance of goal from reward space
                goal_dist = self.entities["goal"].distance(reward_loc)
                # Goal is in reward space, reward goal
                if goal_dist == 0:
                    # Set reward space as goal
                    rewards[reward] = self.entities["agent"].rewards["goal"]
                    # Continue because goal has precedence over any other occupying object
                    continue
                # Goal is next, reward proximity to goal
                elif goal_dist == 1:
                    rewards[reward] = self.entities["agent"].rewards["goal_nearby"]
                # Check all obstacle and goal locations
                for obstacle in self.entities["uav"] + self.entities["entity"]:
                    # Get distance of obstacle from reward space
                    obst_dist = obstacle.distance(reward_loc)
                    # Obstacle exists in reward space
                    if obst_dist == 0:
                        # Set reward to presence of static/dynamic obstacle
                        rewards[reward] = self.entities["agent"].rewards["entity"]
                        break
                    # Obstacle exists adjacent to reward space and goal is not in adjacent space
                    elif obst_dist == 1 and goal_dist >= 1:
                        # Set reward to nearby presence of static/dynamic obstacle
                        rewards[reward] = self.entities["agent"].rewards["entity_nearby"]
        # Update rewards in agent
        self.entities["agent"].update_rewards(rewards)

    # Function which checks all entity locations for overlap
    def detect_collisions(self):
        # Check dynamic obstacle locations against all static locations (NOTE: adversaries "move" first)
        for uav in self.entities["uav"]:
            # Check against static obstacles
            for obstacle in self.entities["entity"]:
                # Collision occurs if 2-D coordinates are equal
                if uav.get_location() == obstacle.get_location():
                    # Call function to handle collisions in uav
                    uav.collision()
            # Check if UAV collided with wall
            x = uav.get_location()[0]
            y = uav.get_location()[1]
            if x < 0 or y < 0 or x >= self.dim or y >= self.dim:
                uav.collision()
        # Check agent if collided with static or dynamic obstacles
        for obstacle in self.entities["entity"] + self.entities["uav"]:
            # Collision occurs if 2-D coordinates are equal
            if self.entities["agent"].get_location() == obstacle.get_location():
                # Call agent collision (and possibly end game?) function if agent collides with obstacle
                self.entities["agent"].collision()
        # Check if the agent collided with a wall
        x = self.entities["agent"].get_location()[0]
        y = self.entities["agent"].get_location()[1]
        if x < 0 or y < 0 or x >= self.dim or y >= self.dim:
            self.entities["agent"].collision()

    # Function to check status of system. NOTE: Only works when system is finished running.
    def get_outcome(self):
        # Return boolean comparison of agent and goal locations
        return (
        self.entities["agent"].get_location() == self.entities["goal"].get_location()) if not self.running else None

    def print_outcome(self):
        if self.get_outcome():
            print("Goal!")
        else:
            print("Crashed - Game Over.")

    def test_sim(self, modelType="Random"):
        self.reset(self.grid_file, modelType)  # create grid world and initialize learning model
        while self.running == True:  # Run learning model until it crashes or reaches goal
            self.step()
        print(self.entities["agent"].game_data.Action_Sequence)  # Print the action sequence if you want
        self.print_outcome()  # Print the outcome of the game

    def generate_training_data(self, Num_Successful_Games, Percentage_Saved_Game=0.5):
        # initialize list of all tuples
        list_game_data = []
        i = 0
        total_num_games = 0
        while i < Num_Successful_Games:  # Run the desired number of games
            self.reset(random_agent_start=True)
            visualize_some_games = False
            if total_num_games % 10000 == 0 and visualize_some_games == True:  # Display the game every 10,000 games
                environment(self).run()
            while self.running == True:
                self.step()
            if self.get_outcome() == True:  # If we reach the goal then save the data
                action_len = len(
                    self.entities["agent"].game_data.Action_Sequence)  # Get the length of the action sequence
                list_game_data.append((action_len, self.entities[
                    "agent"].game_data))  # make a tuple....first element = length of action sequence, second is an instance of a class inside a tuple
                i += 1  # Yay we got a successful game!
            total_num_games += 1  # Keep track of the total number of run games... just for curiosity
        # sort list of tuples by the value of the first element in each tuple
        list_game_data.sort()
        # make a list of only the top X% of games
        list_best_data = list_game_data[0:math.ceil(len(list_game_data) * Percentage_Saved_Game)]
        # remove the first element of the tuple (the action sequence length) because we don't need to save that info
        best_data = []
        for i in range(len(list_best_data)):
            best_data.append(list_best_data[i][1])
        # Save the data
        self.save_training_data(best_data)

    def save_training_data(self, list_game_data):  # TODO
        # Dumping the data in Python specific format

        with open('data.pickle', 'wb') as x:
            pickle.dump(list_game_data, x)

		# Code to Extract Data

        # with open('data.pickle', 'rb') as x:
        #     self.data = pickle.load(x)
        #
        # print(self.data)

if __name__ == "__main__":
    world_instance = system("SingleAgent.txt","Random")

    # world_instance.test_sim()
    world_instance.generate_training_data(60000)