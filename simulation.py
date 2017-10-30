"""
Name: Simulation - run this script to run the project simulation

Project: UAV Obstacle Avoidance Using Q-Learning Techniques

Authors: Katherine Glasheen, Marc Gonzalez, Shayon Gupta, 
Travis Hainsworth, Ramya Kanlapuli


"""
import numpy as np
import agent
import uav
import sys
#environment class/functions?
#def 

# define a model dictionary, which maps user inputs of learning model names to learning model function
modelType = {"random":predict_random,"standard":predict_standard,"NN":predict_NN}


if __name__ == "__main__":
	#-------for unit tests----------
	start = np.array([[0,0]])
	goal = np.array([[5,5]]) 
	obstacle = [[1,1] [5,5]]
	#-----------------------------------
	# initialize grid world (grid size, obstacle locations, start location, goal location)
	#........Shayon's contributions..........
	
	# initalize vehicle position
	vehState = start
	
	# initialize agent class and uav class
	agent=agent(vehState)
	#UAV = uav()
	
	# initialize decision model (options = "random", "standard", or "NN")
	model = "standard" # will be a user input

	
	try:
		# while the agent is not located at the goal position:
		while vehState.all() != goal.all():
			#------------------------------------------
			# make observations
			#obs = observe(vehState)
			obs = [0, 0, 0, 0] #for testing
			# decide what action to take
			action_commanded = modelType[model](vehState,obs)
			# command action (employ dynamics)
			vehState = move(location, action_commanded) # is location an argument to this?
			#------------------------------------------

		# if vehicle is in an obstacle grid space, quit and output "Mission Failed"
			if vehState.all() == obstacle.any():
				print ("Mission Failed")
				break 
			else:
				pass
		# store hstory of states		
	except KeyboardInterrupt:
		print("Interrupted")
		
		#store history of state and commanded action as text files
		sys.exit(0)
					 

