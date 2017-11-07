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
	def __init__(self, grid_file):
		self.grid_file = grid_file
		# Set simulation entities to initial conditions from file
		self.reset(self.grid_file)
		
	# Function to reset the state of the system from input file
	def reset(self, grid_file=None):
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
				if object_type == "agent": self.entities["agent"] = agent([row, col])
				elif object_type == "goal": self.entities["goal"] = entity([row, col])
				elif object_type == "uav": self.entities["uav"].append(uav([row, col]))
				elif object_type == "entity": self.entities["entity"].append(entity([row, col]))
	
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
		self.entities["agent"].move()
		# Perform collision detection
		self.detect_collisions()
		# Check if UAV made it to goal
		if self.entities["agent"].get_location() == self.entities["goal"].get_location():
			#TODO: Write ending function, including saving model or restarting
			pass
		
	# Function which checks all entity locations for overlap
	def detect_collisions(self):
		# Check dynamic obstacle locations against all static locations (NOTE: adversaries "move" first)
		for uav in self.entities["uav"]:
			# Check against static obstacles
			for obstacle in self.entities["static"]:
				# Collision occurs if 2-D coordinates are equal
				if uav.get_location() == obstacle.get_location():
					# Call function to handle collisions in uav
					uav.collision()
		# Check agent if collided with static or dynamic obstacles
		for obstacle in zip(self.entities["entity"], self.entities["uav"]):
			# Collision occurs if 2-D coordinates are equal		
			if self.entities["agent"].get_location() == obstacle.get_location():
				# Call agent collision (and possibly end game?) function if agent collides with obstacle
				self.entities["agent"].collision()
				
	# Function to train agent model
	def train_model(self):
		#TODO
		pass
		
	# Function to test agent model
	def test_model(self):
		#TODO
		pass
