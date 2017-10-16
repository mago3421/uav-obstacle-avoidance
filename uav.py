"""
Name: UAV class

Project: UAV Obstacle Avoidance Using Q-Learning Techniques

Authors: Katherine Glasheen, Marc Gonzalez, Shayon Gupta, 
Travis Hainsworth, Ramya Kanlapuli
	
Description: This class extends the entity object to create
a UAV in the simulation including dynamics and path planning.
"""

from entity import *

class uav(entity):

	# Initializer function
	def __init__(self,location):
		super.__init__(location)
		# Initialize velocity according components in location
		self.v = []
		for comp in range(len(location)):
			self.v.append(0)
		
	
