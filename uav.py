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

class uav(entity):

	# Initializer function
	def __init__(self,location):
		# Initialize entity super-class
		super.__init__(location)
		# Initialize velocity according components in location
		self.v = []
		# Initialize current heading
		self.heading = "none"
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
							
	# Move function
	def move(self, command):
		# Move if UAV command was successful, else stay put
		if random() > self.dynamics[command][self.heading]:
			# Move according to command (up/down -> y+/-1, left/right -> x-/+1)
			if command == "up": location[1] += 1
			if command == "down": location[1] -= 1
			if command == "left": location[0] -= 1
			if command == "right": location[0] += 1
			#TODO: Perform bounds check to make sure UAV does not move outside grid
			#location[0] = location[0] if 
			#location[1] = location[1] if 
		# UAV changes heading regardless if move was successful
		self.heading = command
		
