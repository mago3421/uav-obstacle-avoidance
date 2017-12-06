"""
Name: Q Matrix Allocation

Project: UAV Obstacle Avoidance Using Q-Learning Techniques

Authors: Katherine Glasheen, Marc Gonzalez, Shayon Gupta,
Travis Hainsworth, Ramya Kanlapuli

Description: This class allocates and updates the values of the Q_matrix. It enables the agent to find its goal using the rewards specified in the Q_Matrix
"""

# Q- matrix
import pickle
import os
from uav import *
import numpy as np
import scipy.io as sio

class Q_matrix:
    
    def __init__(self, dimensions):
        self.grid_sz = dimensions #first line of singleagent.txt
        self.cells = self.grid_sz*self.grid_sz
        self.num_actions = 4
        self.alpha = .01 # learning rate
        self.gamma = 0.1 # discount factor
        if os.path.isfile('q_dump.pickle'):
            # with open('q_dump.pickle', 'rb') as x:
            #     self.Q = pickle.load(x)
            if os.path.getsize('q_dump.pickle') > 0:
                with open('q_dump.pickle', 'rb') as f:
                    unpickler = pickle.Unpickler(f)
                    self.Q = unpickler.load()
        else:
            # self.Q = np.zeros((self.cells, self.num_actions))
            self.Q = np.random.random((self.cells, self.num_actions))
            # self.Q = sio.loadmat('QContents.mat')['Q_matrix']




        
        
    #def initialize(self):
        
    # location = self.entities["agent"],
    # rewards = self.rewards or self.los
    
    def update(self,location,los):
        st = location[0]*self.grid_sz + location[1] # Each location is written as (5,7) - 5*10+7 = 57th row of the Q matrix, which has 4 columns that has the actions associated with it
        for i in range(self.num_actions): #number of actions # this loop is to propagate the agent forward to help populate the matrix
            if i == 0:   #action is up
                st_new = location[0]*self.grid_sz + location[1]+1
                act = "up"
            elif i == 1: #action is down
                st_new = location[0]*self.grid_sz + location[1]-1
                act = "down"
            elif i == 2:   #action is left
                st_new = (location[0]-1)*self.grid_sz + location[1]
                act = "left"
            elif i == 3: #action is right
                st_new = (location[0]+1)*self.grid_sz + location[1]
                act = "right"
            # DEBUG: Hacked to get running     
          #  try:
                # the Q matrix is strutured in a way where each state has Q values for each action associated with that state
            self.Q[st,i] = (1-self.alpha)*self.Q[st,i] + self.alpha*(los[act] + self.gamma*max(self.Q[st_new,:]))
                # a = self.Q.index(max(self.Q[st,:]))
            a = np.where(self.Q[st,:] == max(self.Q[st,:])) # we pick the index of the max Q value associated with the action for a particular state
            a = a[0][0] # This is because np.where returns an array and we need a value
        
            if a ==0: # Associating the index( a number) with a verbal command
                command = "up"
            elif a==1:
                command = "down"
            elif a==2:
                command = "left"
            elif a==3:
                command = "right"
        return command
          #  except IndexError:
          #  print("IndexError")
          #  return "up" #DEBUG: Fix
    
    def reset_Q(self):
        # self.Q = np.zeros((self.cells, self.num_actions))
        self.Q = np.random.random((self.cells, self.num_actions))
        # self.Q = sio.loadmat('QContents.mat')['Q_matrix']

        with open('q_dump.pickle', 'wb') as x:
            pickle.dump(self.Q, x)

    def dump_Q(self):
        # os.remove('q_dump.pickle')
        with open('q_dump.pickle', 'wb') as x:
            pickle.dump(self.Q, x)

    def load_Q(self):

        # with open('q_dump.pickle', 'rb') as x:
        #     self.Q = pickle.load(x)

        if os.path.getsize('q_dump.pickle') > 0:
            with open('q_dump.pickle', 'rb') as f:
                unpickler = pickle.Unpickler(f)
                # if file is not empty scores will be equal
                # to the value unpickled
                self.Q = unpickler.load()
