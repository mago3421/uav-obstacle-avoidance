"""
Name: Agent class

Project: UAV Obstacle Avoidance Using Q-Learning Techniques

Authors: Katherine Glasheen, Marc Gonzalez, Shayon Gupta, 
Travis Hainsworth, Ramya Kanlapuli
	
Description: This class extends the uav object to create
the agent in the simulation including Q-score and learning model.
"""

from uav import *

class agent(uav):
	
	# Intializer function
	def __init__(self, location):
		# Initialize uav super-class
		super.__init__(location)
		# Initialize learning model
		self.model = None
		
	# Function which predicts next movement based on learning model
	def predict(self):
		pass
		
