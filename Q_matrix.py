# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 09:20:59 2017

@author: ramya
"""

# Q- matrix
from uav import *

class Q_matrix:
    
    def __init__(self, dimensions):
        self.grid_sz = dimensions #first line of singleagent.txt
        self.cells = self.grid_sz*self.grid_sz
        self.num_actions = 4
        self.alpha = 0.1
        self.gamma = 0.75
        self.Q = np.zeros((self.cells,self.num_actions))
        
        
    #def initialize(self):
        
    # location = self.entities["agent"],
    # rewards = self.rewards or self.los
    
    def update(self,location,los):
        st = location[0]*self.grid_sz + location[1]
        for i in range(self.num_actions): #number of actions
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
                    
            self.Q[st,i] = (1-self.alpha)*self.Q[st,i] + self.alpha*(los[act] + self.gamma*max(Q[st_new,:]))
        
        a = self.Q.index(max(self.Q[st,:])) 
		
        if a ==0: 
            command = "up"
        elif a==1:
            command = "down"
        elif a==2:
            command = "left"
        elif a==3:
            command = "right"
		
        return command
    
    def reset_Q(self):
        self.Q = np.zeros(self.cells,self.num_actions)

        
        