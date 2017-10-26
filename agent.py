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
		
	# Function which gathers observations based on current position. Should return a matrix with the 
	def observe(self):
		pass

	# Function to generate rewards using observations and lookup table (create reward dict inside fxn?)
	def generateRewards(self):
		pass
	
	# Function which takes in observations, rewards, and former Q-matrix and outputs the action that yields maximum Q using the standard method
	def predict_standard(self):
		return action		
		
	# Function which predicts next movement based on neural network learning model
	def predict_NN(self):
		return action
		
