﻿"""
Name: Agent class

Project: UAV Obstacle Avoidance Using Q-Learning Techniques

Authors: Katherine Glasheen, Marc Gonzalez, Shayon Gupta, 
Travis Hainsworth, Ramya Kanlapuli
	
Description: This class extends the uav object to create
the agent in the simulation including Q-score and learning model.
"""

from uav import *
from numpy import random
#from neural_network import *

class agent(uav):
	
	# Intializer function
	def __init__(self, location, learning_model="Random"):
		# Initialize uav super-class
		super(agent,self).__init__(location)
		self.Q = None#Q matrix, initialized as 3D matrix
		self.R = None#initialize R matrix
		# Initialize learning model
		self.model = learning_model
		# Initialize health
		self.crashed = False

		# Initialize game data sequences
		self.Action_Sequence = []
		self.Position_Sequence = []
		self.Reward_Sequence = []
		
	# Function which gathers observations based on current position. Should return a matrix with the 
	def observe(self):
	    #Update Q matrix here, appendable dictionary?
	    pass

	# Function which takes in observations, rewards, and former Q-matrix and outputs the action that yields maximum Q using the standard method
	# main loop make location and rewards random and test
	# Haven't defined proper variable names, in development
	def predict_Standard(self, location, rewards):
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
	def predict_Random(self):
		rd = random.random() # Make a random number
		possibleActions = [] # An array of possible actions that won't lead to the wall
		if self.los["up"] >-100:          # Note self.los is the dictionary of rewards! Not sure why it is called that...
			possibleActions.append("up")  # and it is updated in the system block
		if self.los["down"] >-100:
			possibleActions.append("down")
		if self.los["left"] >-100:
			possibleActions.append("left")
		if self.los["right"] >-100:
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
			command = self.predict_Random()
		elif self.model == "Standard":
			command = self.predict_Standard(self.location,self.los) # Not sure on rewards...
		else:
			command = self.predict_NN(self.location,self.los) # Not sure on rewards...

		# Move if UAV command was successful, else stay put
		if random.random() > self.dynamics[command][self.heading]:
			if command == "up": self.location[1] += 1 
			if command == "down": self.location[1] -= 1
			if command == "left": self.location[0] -= 1
			if command == "right": self.location[0] += 1

		self.Action_Sequence.append(command) # TODO maybe adding these should be optional?
		self.Position_Sequence.append(self.location)  
		self.Reward_Sequence.append(self.los)