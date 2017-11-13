"""
Name: Entity class

Project: UAV Obstacle Avoidance Using Q-Learning Techniques

Authors: Katherine Glasheen, Marc Gonzalez, Shayon Gupta, 
Travis Hainsworth, Ramya Kanlapuli
	
Description: This class implements a generic physical object
in the simulation including basic physical attributes and
graphical representation.
"""

import math

class entity:

	# Initializer function
	def __init__(self, location):
		# Initialize location in grid as list
		self.location = location
	
	# Return location
	def get_location(self):
		return self.location
		
	# Set location
	def set_location(self, new_location):
		self.location = new_location if len(self.location) == len(new_location) else self.location

	# Return distance of entity location from target
	def distance(self, other):
		magnitude = 0
		# Assumes distance vectors are the same dimension
		for i,j in zip(self.location, other):
			# Get magnitude of difference vector
			magnitude += pow(abs(i-j),2)
		return math.sqrt(magnitude)
		
