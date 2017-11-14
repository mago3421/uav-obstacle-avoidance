"""
Name: UAV class

Project: UAV Obstacle Avoidance Using Q-Learning Techniques

Authors: Katherine Glasheen, Marc Gonzalez, Shayon Gupta, 
Travis Hainsworth, Ramya Kanlapuli
	
Description: This class extends the entity object to create
a UAV in the simulation including dynamics and path planning.
"""

from entity import *
from numpy.random import random
import numpy as np

class uav(entity):

	# Initializer function
	def __init__(self,location):
		# Initialize entity super-class
		super(uav,self).__init__(location)
		# Initialize velocity according components in location
		self.v = []
		# Initialize current heading
		self.heading = "right"
		# Vehicle dynamics 2-D dictionary
		self.dynamics = {"up": 
							{"up": 0.75,
							 "down": 0.05,
							 "left": 0.10,
							 "right":0.10,},
						"down": 
							{"up": 0.05,
							 "down": 0.75,
							 "left": 0.10,
							 "right":0.10,},
						"left": 
							{"up": 0.10,
							 "down": 0.10,
							 "left": 0.75,
							 "right":0.05,},							
						"right": 
							{"up": 0.10,
							 "down": 0.10,
							 "left": 0.05,
							 "right":0.75,}}

		self.rewards = {"goal":100, 
						"goal_nearby":10, 
						"entity":-100, 
						"entity_nearby":-10, 
						"oob":-50, 
						"empty": 0}
						
		self.los = {"up":0, "down":0, "left":0, "right":0}

		
		# Initialize health
		self.crashed = False
							
	# Move function
	def move(self): 
		# Insert logic to choose command
		command = "up"
		# Move if UAV command was successful, else stay put
		if random() > self.dynamics[command][self.heading]:
			# Move according to command (up/down -> y+/-1, left/right -> x-/+1)
			if command == "up": self.location[1] += 1
			if command == "down": self.location[1] -= 1
			if command == "left": self.location[0] -= 1
			if command == "right": self.location[0] += 1
			#TODO: Perform bounds check to make sure UAV does not move outside grid
			#location[0] = location[0] if 
			#location[1] = location[1] if 
		# UAV changes heading regardless if move was successful
		self.heading = command
		# Don't think we need to return location
		#return self.location
		
	# Function which gathers observations based on current position. Should return a matrix with the 
	def observe(self, obsHorizon):
		rewards = obsHorizon # initialize so it is the same length
		for j in range(0,len(obsHorizon)):
			rewards[j] = self.rewards[obsHorizon[j]] 
			#print (self.rewards[obsHorizon[j]]) 
		rewards = np.asarray(rewards)
		return rewards
		
	# Function to update rewards dictionary of UAV
	def update_rewards(self, rewards):
		# Assume keys are the same
		for key in rewards.keys():
			self.los[key] = rewards[key]

		# Collision function
	def collision(self):
		self.crashed = True


if __name__ == "__main__":
	obsHor = ["!","^", "*","-","#","~"]
	loc = [2,2]
	UAV=uav(loc)

	rew = UAV.observe(obsHor)
	print("rew = ", rew)
