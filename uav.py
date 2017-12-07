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
		# Initialize health
		self.crashed = False
							
	# Move function
	def move(self): 
		# Insert logic to choose command
		command = "up"
		# Save last location for collision detection
		self.last_location = self.location
		# Move if UAV command was successful, else stay put
		if random() > self.dynamics[command][self.heading]:
			# Move according to command (up/down -> y+/-1, left/right -> x-/+1)
			if command == "up": self.location[1] += 1
			if command == "down": self.location[1] -= 1
			if command == "left": self.location[0] -= 1
			if command == "right": self.location[0] += 1
		# UAV changes heading regardless if move was successful
		self.heading = command


	# Collision function for UAV returns it to previous location and sets heading in opposite direction
	def collision(self):
		# Get direction of movement
		dx = self.location[0] - self.last_location[0]
		dy = self.location[1] - self.last_location[1]
		# Set location to last location and leave last location to indicate it has spent two turns there
		self.location = self.last_location
		# Right movement, move left instead
		if dx > 0: self.heading = "left"
		# Left movement, move right instead
		elif dx < 0: self.heading = "right"
		# Up movement, move down instead
		elif dy > 0: self.heading = "down"
		# Down movement, move up instead
		elif dy < 0: self.heading = "up"


if __name__ == "__main__":
	obsHor = ["!","^", "*","-","#","~"]
	loc = [2,2]
	UAV=uav(loc)

	rew = UAV.observe(obsHor)
	print("rew = ", rew)
