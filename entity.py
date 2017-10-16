"""
Name: Entity class

Project: UAV Obstacle Avoidance Using Q-Learning Techniques

Authors: Katherine Glasheen, Marc Gonzalez, Shayon Gupta, 
Travis Hainsworth, Ramya Kanlapuli
	
Description: This class implements a generic physical object
in the simulation including basic physical attributes and
graphical representation.
"""

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
