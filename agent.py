"""
Name: Agent class
Project: UAV Obstacle Avoidance Using Q-Learning Techniques
Authors: Katherine Glasheen, Marc Gonzalez, Shayon Gupta,
Travis Hainsworth, Ramya Kanlapuli

Description: This class extends the uav object to create
the agent in the simulation including Q-score and learning model.
"""
import os
from uav import *
from Q_matrix import *
from numpy import random
from numpy import array
from numpy import argmax
#from neural_network import *
from keras.models import load_model
from game_data import *

class agent(uav):

	# Intializer function
	def __init__(self, location, learning_model="Random", enemy=False):
		# Initialize uav super-class
		super(agent,self).__init__(location)
#		self.Q = Q#Q matrix, initialized as 3D matrix
#		self.R = R#initialize R matrix
		# Initialize learning model
		self.model = learning_model
		# Initialize health
		self.crashed = False

		# Initialize game data sequences
		self.game_data = game_data_class()

		# If the agent is using Neural network then initialize the model
		self.NN_model_file = 'neural_network_model.h5'
		if learning_model == "NN":
			self.NN_model = load_model(self.NN_model_file)

		# Initialization of standard model
		if learning_model == "Standard":
			if enemy == False:
				Q_Matrix_Pickle_File = 'q_dump.pickle'
			else: # The agent is an adversary/obstacle
				Q_Matrix_Pickle_File = 'q_dump_enemy.pickle'
			self.qObj = Q_matrix(10,Q_Matrix_Pickle_File)
			if os.path.isfile(Q_Matrix_Pickle_File):
				self.qObj.load_Q()
			else:
				self.qObj.reset_Q()

	# Function which takes in observations, rewards, and former Q-matrix and outputs the action that yields maximum Q using the standard method
	# main loop make location and rewards random and test
	# Haven't defined proper variable names, in development
	def predict_Standard(self, location, rewards):
		command = self.qObj.update(location, rewards)
		self.qObj.dump_Q()
		print('updating')
		return command
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

		# one hot encode input:
		input = []
		input.extend(location)
		input.append(rewards["up"])
		input.append(rewards["down"])
		input.append(rewards["left"])
		input.append(rewards["right"])

		# process output:
		output = self.NN_model.predict(array([input])) # Not sure why the syntax has to be this way to get the correct shape for the initial dense layer.
		index = argmax(output[0]) # get the index of the most correct action
		if index == 0:
			command = "up"
		elif index == 1:
			command = "down"
		elif index == 2:
			command = "left"
		else:
			command = "right"
		return command

	# Function which predicts next movement based on Random Movement
	def predict_Random(self):
		rd = random.random() # Make a random number
		possibleActions = [] # An array of possible actions that won't lead to the wall
		wall_reward = -1000
		if self.los["up"] > wall_reward:          # Note self.los is the dictionary of rewards! Not sure why it is called that...
			possibleActions.append("up")  # and it is updated in the system block
		if self.los["down"] > wall_reward:
			possibleActions.append("down")# TODO Maybe make this a truly random (trade off between more games and better games when training NN)
		if self.los["left"] > wall_reward:
			possibleActions.append("left")
		if self.los["right"] > wall_reward:
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
			command = self.predict_NN(self.location,self.los)

		# Move if UAV command was successful, else stay put
		if random.random() > self.dynamics[command][self.heading]:
			if command == "up": self.location[1] += 1
			if command == "down": self.location[1] -= 1
			if command == "left": self.location[0] -= 1
			if command == "right": self.location[0] += 1

		self.game_data.update(command,self.location,self.los) # TODO maybe adding these should be optional?

	# Change the base model of the NN agent
	def set_NN_model(self, NN_model_file):
		if self.model != "NN":
			print('This function is for use with the Neural Network Agent')
		else:
			self.NN_model_Name = NN_model_file
			self.NN_model = load_model(self.NN_model_file)
	

