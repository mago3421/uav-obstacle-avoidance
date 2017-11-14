"""
Name: Agent class

Project: UAV Obstacle Avoidance Using Q-Learning Techniques

Authors: Katherine Glasheen, Marc Gonzalez, Shayon Gupta, 
Travis Hainsworth, Ramya Kanlapuli
	
Description: This class extends the uav object to create
the agent in the simulation including Q-score and learning model.
"""

from uav import *
from numpy import random
from neural_network import *

class agent(uav):
	
	# Intializer function
	def __init__(self, location, learning_model="Random"):
		# Initialize uav super-class
		super.__init__(location)
		self.Q = None#Q matrix, initialized as 3D matrix
		self.R = None#initialize R matrix
		# Initialize learning model
		self.model = learning_model
		# Initialize health
		self.crashed = False
		
	# Function which gathers observations based on current position. Should return a matrix with the 
	def observe(self):
	    #Update Q matrix here, appendable dictionary?
	    
		pass

	# Function to generate rewards using observations and lookup table (create reward dict inside fxn?)
	def getRewards(self):
		pass
	
	# Function which takes in observations, rewards, and former Q-matrix and outputs the action that yields maximum Q using the standard method
	# main loop make location and rewards random and test
	# Haven't defined proper variable names, in development
	def predict_standard(self):
		pass
		"""
	    for i in range(horizon) #horizon is 4
	    
	    Q[location[0],location[1],action] = (1-alpha)*Q[location[0],location[1],action] + alpha*[Reward[location[0],location[1],action]] + gamma*max(Q[location_new[0],location_new[1],:]) 
	    
	    a = Q.index(max(Q[location[0],location[1],:])) 
	    
	    if a ==1 
	        command = "up"
	    elif a==2
	        command = "down"
	    elif a==3
	        command = "left"
	    elif a==4
	        command = "right"
	    
		return command	
		"""
	# Function which predicts next movement based on neural network learning model
	def predict_NN(self, location, rewards):
		command = "up" # Filler command for now
		return command

	# Function which predicts next movement based on Random Movement
	def predict_Random(self,Current_Location=[0,0],Possible_Rewards=[0,0,0,0]):
		rd = random.random() # Make a random number
		possibleActions = [] # An array of possible actions that won't lead to the wall
		if Possible_Rewards[0] >-100:
			possibleActions.append("up")
		if Possible_Rewards[1] >-100:
			possibleActions.append("down")
		if Possible_Rewards[2] >-100:
			possibleActions.append("left")
		if Possible_Rewards[3] >-100:
			possibleActions.append("right")

		# Select a random action from the list of possible actions
		probabilityIncrement = 1/len(possibleActions)
		for i in range(len(possibleActions)-1):
			if rd < probabilityIncrement*(i+1):
				return possibleActions[i]
		return possibleActions[-1] # Last element in the array of possible actions
		
	# Collision function
	def collision(self):
		self.crashed = True
		
	def check_crash(self):
		return self.crashed

	def move(self):
		if self.model == "Random":
			return self.predict_Random()
		if self.model == "Standard":
			return self.predict_Standard(self.location,self.los) # Not sure on rewards...
		else:
			return self.predict_NN(self.location,self.los) # Not sure on rewards...
		
