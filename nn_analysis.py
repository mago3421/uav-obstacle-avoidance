from system import *
from environment import *
import matplotlib.pyplot as plt


# File to plot the success rate of a NN model (number of times the
# goal is reached/number of attempts)
#
# And for successful games we plot the optimality of the found paths
# (optimal path length / actual path length) 

# Want to visualize some of the games? set this as true!
visualize_some_games = True
 
# Define How many games you would like each model to run
Games_To_Play = 1000

# create a system 
sys = system("SingleAgent.txt", modelType = "NN", max_step_count = 100)

# Define the optimal path length for "SingleAgent.txt" based on starting position
Optimal_Path_Length_Dict = {
	(0,0):7, (0,1):6, (0,2):5, (0,3):6, (0,4):5, (0,5):6, (0,6):7, (0,7):8, (0,8):9, (0,9):10,
	(1,0):6, (1,1):5, (1,2):4, (1,3):5, (1,4):4, (1,5):5,          (1,7):9, (1,8):8, (1,9):9,
             (2,1):4, (2,2):3, (2,3):4, (2,4):3, (2,5):4,                   (2,8):7, (2,9):8,
	(3,0):4, (3,1):3, (3,2):2,          (3,4):2, (3,5):3,          (3,7):5, (3,8):6, (3,9):7,
             (4,1):2, (4,2):1, (4,3):0, (4,4):1, (4,5):2, (4,6):3, (4,7):4, (4,8):5, (4,9):4,
	(5,0):6,          (5,2):2, (5,3):1, (5,4):2, (5,5):3, (5,6):4, (5,7):5, (5,8):6, (5,9):7,
    (6,0):5, (6,1):4, (6,2):3, (6,3):2, (6,4):3, (6,5):4, (6,6):5, (6,7):6, (6,8):7, (6,9):8,
    (7,0):6, (7,1):5, (7,2):4, (7,3):3,          (7,5):5, (7,6):6, (7,7):7, (7,8):8, (7,9):9,
             (8,1):6, (8,2):5, (8,3):4, (8,4):5, (8,5):6, (8,6):7, (8,7):8, (8,8):9, (8,9):10, 
	(9,0):8, (9,1):7, (9,2):6, (9,3):5, (9,4):6, (9,5):7, (9,6):8, (9,7):9, (9,8):10,(9,9):11}

# Create data holders
Number_Of_Success = []
Optimality = []
Training_Number = []
# run however many models you would like
for i in range(0,11):
	Training_Number.append((i*60+60)*1000) # Training numbers increment by 60 thousand
	model_name = 'neural_network_model_%dthsnd.h5' % ((i+10)*60+60)

	print('Beginning model with ', Training_Number[i], 'training examples')

	Number_Of_Success.append(0) # we will += 1 for every success of this model
	Optimality.append(0)        # we will be averaging these on a model basis

	# run the model desired number of times and measure the path length
	for run in range(0,Games_To_Play):
		# Reset and run the system instance with the new NN agent
		sys.reset(random_agent_start=True,NN_Model_File=model_name)

		if visualize_some_games == True and run % 100 == 0:
			environment(sys).run()
		else:
			sys.test_sim(Reset_Sim = False, verbose = False)

		# Check success of the run
		if sys.get_outcome() == True:  # We reached the goal
			Number_Of_Success[i] += 1
			# figure out optimality of success
			Optimal_Path_Length = Optimal_Path_Length_Dict[sys.entities["agent"].game_data.Initial_Position_Tuple]
			Actual_Path_Length = len(sys.entities["agent"].game_data.Action_Sequence)
			Optimality[i] += Optimal_Path_Length/Actual_Path_Length # Add the efficiency of this run (we will average later)

		if run % 10 == 0:
			print(run, ' out of ', Games_To_Play)

	# Average the performance
	if Number_Of_Success[i] != 0:
		Optimality[i] /= Number_Of_Success[i]
	Number_Of_Success[i] /= Games_To_Play

	print('Number of Successes: ', Number_Of_Success[i])
	print('Optimality of Successes: ', Optimality[i])

# Plot all of the results
plt.figure(1)
plt.plot(Training_Number,Number_Of_Success)
plt.xlabel('Number of Training Games')
plt.ylabel('Rate of Reaching the Goal (%)')
plt.title('Success Rate based on Training Size')
plt.savefig('Success_Plot.png')

plt.figure(2)
plt.plot(Training_Number,Optimality)
plt.xlabel('Number of Training Games')
plt.ylabel('Average Path Length Efficiency for Successful Games (%)')
plt.title('Path Optimality Based on Training Size')
plt.savefig('Optimality_Plot.png')

plt.show()
