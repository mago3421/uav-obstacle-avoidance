"""
Name: System class

Project: UAV Obstacle Avoidance Using Q-Learning Techniques

Authors: Katherine Glasheen, Marc Gonzalez, Shayon Gupta, 
Travis Hainsworth, Ramya Kanlapuli
	
Description: This class serves as the driver for running the
system simulation including training and testing the agent's model
"""

from visualizer import *
from entity import *
from uav import *
from agent import *

class system:

	# Function to initialize system
	def __init__(self, f):
		# Set simulation entities to initial conditions from file
		self.reset(f)
		
	# Function to reset the state of the system from input file
	def reset(self, f):
		

	# Function which evolves the system by one timestep
	def step(self):
		# Move dynamic obstacles
		for uav in self.entities["dynamic"]: uav.move()
		# Move agent
		self.entities["agent"].move()
		# Perform collision detection
		self.detect_collisions()
		
	# Function which checks all entity locations for overlap
	def detect_collisions(self):
		# Check dynamic obstacle locations against all entities
		for uav in self.entities["dynamic"]:
			# Check against static obstacles
			for loc in self.entities["static"].location:
				# Collision occurs if 2-D coordinates are equal
				if uav.location[0] == loc[0] and uav.location[1] == loc[1]:
					# Call function to handle collisions in uav
					uav.collision()
		# Check agent location against all static and dynamic obstacles

	# Function to train agent model
	def train_model(self):
		
