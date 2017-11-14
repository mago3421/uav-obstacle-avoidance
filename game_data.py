"""
Name: game_data class

Project: UAV Obstacle Avoidance Using Q-Learning Techniques

Authors: Katherine Glasheen, Marc Gonzalez, Shayon Gupta, 
Travis Hainsworth, Ramya Kanlapuli
	
Description: This class serves as a container for the data created
from running a game
"""

class game_data:
	def __init__(self,Action_Sequence=[],Position_Sequence=[],Reward_Sequence=[]):
		self.Action_Sequence=Action_Sequence
		self.Position_Sequence = Position_Sequence
		self.Reward_Sequence = Reward_Sequence

	def update(self,Action,Position,Reward):
		self.Action_Sequence.append(Action)
		self.Position_Sequence.append(Position)
		self.Reward_Sequence.append(Reward)