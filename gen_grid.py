"""
Name: Grid generation script

Project: UAV Obstacle Avoidance Using Q-Learning Techniques

Authors: Katherine Glasheen, Marc Gonzalez, Shayon Gupta, 
Travis Hainsworth, Ramya Kanlapuli
	
Description: This file implements a function to generate a random
grid for model training or testing. This script takes in several
user parameters: dimension (square only), density of static
obstacles, number of dynamic obstacles (enemy UAVs), and filename 
(defaults to environment-[i].txt where i is the zero-indexed number
of environments present in the directory).
"""

from argparse import ArgumentParser as parser
from numpy.random import randint
from os.path import exists

def gen_grid(dim, rho, num_uavs, filename):
	# Check if default filename exists
	i = 0
	# Enumerate default filename if it already exists
	if filename == "Environment-0.txt":
		while exists(filename):
			filename = "Environment-%i.txt"%(i)
			i+=1
	else:
		while exists(filename):
			filename+='(%d)'%(i)
			i+=1
	# Randomly generate agent location
	agent_loc = [randint(0,dim-1), randint(0,dim-1)]
	# Generate goal on opposite side (NOTE: Should we make this random too, i.e., allow for easy course?)
	goal_loc = [abs(agent_loc[0]-((dim-1) * (randint(0,dim-1) % 2))), 
				abs(agent_loc[1]-((dim-1) * (randint(0,dim-1) % 2)))]
	# Ensure goal and agent do not share any indices
	while goal_loc[0] == agent_loc[0]: goal_loc[0] = randint(0, dim-1)
	while goal_loc[1] == agent_loc[1]: goal_loc[1] = randint(0, dim-1)
	# Generate hash table of locations of all entities on grid
	object_locs = {agent_loc[0]:{agent_loc[1]:"agent"}, goal_loc[0]:{goal_loc[1]:"goal"}}
	num_entities = int(rho * dim * dim)
	# Generate locations of entities
	for i in range(0, num_entities):
		# Generate random indices until empty spot is found
		while True:
			row = randint(0, dim-1)
			col = randint(0, dim-1)
			if row in object_locs.keys():
				if not col in object_locs[row].keys():
					object_locs[row][col] = "entity"
					break
			else:
				object_locs[row] = {col:"entity"}
				break
		# Add location of static obstacle to hash table
		object_locs[row][col] = "entity"
	# Generate locations of uav obstacles
	for i in range(0,num_uavs):
		# Generate random indices until empty spot is found
		while True:
			row = randint(0, dim-1)
			col = randint(0, dim-1)
			if row in object_locs.keys():
				if not (col in object_locs[row].keys()):
					object_locs[row][col] = "uav"
					break
			else:
				object_locs[row] = {col:"uav"}
				break
		# Add location of dynamic obstacle to hash table
		object_locs[row][col] = "uav"
	# Open file
	f = open(filename, 'w')
	# Write square dimension size at top
	f.write(str(dim)+'\n')
	# Write agent location to file
	# Write each object and its location from hash table
	for row in object_locs.keys():
		for col in object_locs[row].keys():
			f.write(object_locs[row][col]+' '+ str(row) + ' ' + str(col) + '\n')
	
# Command line script
if __name__ == "__main__":
		# Initialize parser
		parser = parser(description='Generate a grid file')
		parser.add_argument('-d', type=int, default=10, help='Length and width of square-grid')
		parser.add_argument('-p', type=int, default=0.15, help='Decimal percentage of grid occupied by static obstacles')
		parser.add_argument('-u', type=int, default=1, help='Number of enemy UAVs in the grid')
		parser.add_argument('-f', type=str, default="Environment-0.txt", help='Designated filename')
		# Get arguments
		args = parser.parse_args()
		# Generate grid using args: dim, rho, num_adv, filename
		gen_grid(args.d, args.p, args.u, args.f)
		
							
