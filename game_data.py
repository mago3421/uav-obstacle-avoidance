"""
Name: game_data_class

Project: UAV Obstacle Avoidance Using Q-Learning Techniques

Authors: Katherine Glasheen, Marc Gonzalez, Shayon Gupta, 
Travis Hainsworth, Ramya Kanlapuli
	
Description: This class serves as a container for the data created
from running a game
"""

class game_data_class:
	def __init__(self,Action_Sequence=[],Position_Sequence=[],Reward_Sequence=[], Initial_Position=[0,0]):
		self.Action_Sequence = Action_Sequence
		self.Position_Sequence = Position_Sequence
		self.Reward_Sequence = Reward_Sequence
		self.Initial_Position = Initial_Position
		self.Initial_Position_Tuple = (Initial_Position[0],Initial_Position[1]) # Dictionaries don't want lists 
		                                               # as keys and I want to have a dictionary of optimal path lengths

	def update(self,Action,Position,Reward):
		self.Action_Sequence.append(Action)
		self.Position_Sequence.append(Position)
		self.Reward_Sequence.append(Reward)

	def update_Initial_Position(self,Initial_Position):
		self.Initial_Position = Initial_Position
		self.Initial_Position_Tuple = (Initial_Position[0], Initial_Position[1])

	def reinitialize(self, Action_Sequence=[],Position_Sequence=[],Reward_Sequence=[], Initial_Position=[0,0]):
		self.Action_Sequence = Action_Sequence
		self.Position_Sequence = Position_Sequence
		self.Reward_Sequence = Reward_Sequence
		self.Initial_Position = Initial_Position
		self.Initial_Position_Tuple = (Initial_Position[0],Initial_Position[1])