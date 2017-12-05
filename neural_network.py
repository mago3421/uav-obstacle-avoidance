"""
Name: neural_network
Project: UAV Obstacle Avoidance Using Q-Learning Techniques
Authors: Katherine Glasheen, Marc Gonzalez, Shayon Gupta,
Travis Hainsworth, Ramya Kanlapuli

Description: This class creates, trains, and saves the neural network
model based on data created from system.py's generate training data 
function. The model is saved as 'neural_network_model.h5'

Note! With broken training data testing and evaluation is not supported
"""

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.callbacks import EarlyStopping
from keras.models import load_model
import numpy as np
import pickle


# Saving and loading info: https://keras.io/getting-started/faq/#how-can-i-save-a-keras-model


def data_read(data_file = 'NN_Training_Data\Single_Agent_0.pickle',data = None, evaluation_percentage=0.05):
	print('Processing Data')
	with open(data_file, 'rb') as x:
		unprocessed_data = pickle.load(x)

	size_of_data_set = len(unprocessed_data)
	if data == None:
		data = data_type()

	game_number = 0

	#### Dealing with broken training data ####
	# Broken training data did not reset the game_data class when games were reset and as such each game contains
	# all of the games that were run (in the beginning cases that included 60,000 sets)
	Broken_Data = True
	if Broken_Data == True:
		unprocessed_data = [unprocessed_data[0]]

	#### Break up the games and one hot encode ####
	for game in unprocessed_data: # Create the training data
		game_number += 1
		input_game = []
		output_game = []

		game_data_length = len(game.Action_Sequence)

		# create an input array for a given game example
		for step in range(game_data_length):
			input_step = []
			input_step.extend(game.Position_Sequence[step]) # Extend takes the content of a list and puts it in another
			input_step.append(game.Reward_Sequence[step]["up"])
			input_step.append(game.Reward_Sequence[step]["down"])
			input_step.append(game.Reward_Sequence[step]["left"])
			input_step.append(game.Reward_Sequence[step]["right"])
		
			input_game.append(input_step) # append the list for a single step to the list of inputs for a game 

			# one hot encode the output for a given game example
			action_step = game.Action_Sequence[step]
			if action_step == "up":
				one_hot_output = [1, 0, 0, 0]
			elif action_step == "down":
				one_hot_output = [0, 1, 0, 0]
			elif action_step == "left":
				one_hot_output = [0, 0, 1, 0]
			else: # action_step == "down"
				one_hot_output = [0, 0, 0, 1]
			output_game.append(one_hot_output)

		# Break up the games to test and training data
		if game_number < size_of_data_set*evaluation_percentage:
			data.test_x.extend(input_game)
			data.test_y.extend(output_game)
		else:
			data.train_x.extend(input_game)
			data.train_y.extend(output_game)

	
	if Broken_Data == True:
		data.train_x = data.test_x[round(evaluation_percentage*len(data.test_x)):-1]
		data.train_y = data.test_y[round(evaluation_percentage*len(data.test_y)):-1]
		data.test_x = data.test_x[0:round(evaluation_percentage*len(data.test_x))]
		data.test_y = data.test_y[0:round(evaluation_percentage*len(data.test_y))]

	return data

# A class to separate training and test data
class data_type():
	def __init__(self):
		self.train_x = []
		self.train_y = []
		self.test_x = []
		self.test_y = []

class NN:
	'''
	NN classifier
	'''
	def __init__(self, train_x, train_y, test_x, test_y, epoches = 15, batch_size=63, model_name = None):
		'''
		initialize NN classifier
		'''
		print('Creating Model')
		self.batch_size = batch_size
		self.epoches = epoches


        # Data Storage
		self.train_x = np.array(train_x)
		self.train_y = np.array(train_y)
		self.test_x = np.array(test_x)
		self.test_y = np.array(test_y)

		if model_name == None:
		    # Model Creation
			self.model = Sequential() # model type recommended: https://www.youtube.com/watch?v=G-KvpNGudLw
			self.model.add(Dense(128, input_dim=len(self.train_x[0]), activation = 'relu')) # I think the shape of these may need to be toyed with?
			self.model.add(Dropout(0.2))
			self.model.add(Dense(256,activation='relu'))
			self.model.add(Dropout(0.2))
			self.model.add(Dense(512,activation='relu'))
			self.model.add(Dropout(0.2))
			self.model.add(Dense(256,activation='relu'))
			self.model.add(Dropout(0.2))
			self.model.add(Dense(128,activation='relu'))
			self.model.add(Dropout(0.2))
			self.model.add(Dense(len(self.train_y[0]),activation='softmax'))
			self.model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
		else:
			self.model = load_model(model_name)

	def train(self):
		'''
        train NN classifier with training data
		according to: https://github.com/fchollet/keras/issues/1868 the weights are not re-written, but merely updated
        :param x: training data input
        :param y: training label input
        :return:
        '''
        # TODO: fit in training data   
		print('Training Model') 
		EarlyStoppingVar = EarlyStopping('val_loss')    
		self.model.fit(self.train_x, self.train_y, self.batch_size, self.epoches, verbose=0, callbacks=[EarlyStoppingVar],validation_split=0.1,shuffle=True)

	def evaluate(self):
		'''
        test NN classifier and get accuracy
        :return: accuracy
        '''
		print('evaluating model')
		acc = self.model.evaluate(self.test_x, self.test_y)
		return acc

    #def update_data(self,train_x, train_y, test_x, test_y):
    #    self.train_x = np.array(train_x)
    #    self.train_y = np.array(train_y)
    #    self.test_x = np.array(test_x)
    #    self.test_y = np.array(test_y)


if __name__ == '__main__':
	# Todo read training data
	counter = 360 # Change for when for loop indices change training file 16 corresponds to counter 360
	for i in range(16,21):
		data = data_type()
		file_name = 'NN_Training_Data\Single_Agent_%d\Single_Agent_%d.pickle' % (i,i)
		data = data_read(file_name,data)

		# Create network
		Create_Model = False # Set a boolean for creating a new model or for adding training to an existing model
		if Create_Model == True:
			nn = NN(data.train_x, data.train_y, data.test_x, data.test_y)
		else:
			model_name = 'neural_network_model_%dthsnd.h5' % (counter)
			nn = NN(data.train_x, data.train_y, data.test_x, data.test_y, model_name = model_name)

		# Train the network and evaluate it
		nn.train()
		acc = nn.evaluate()
		print(acc)

		# save the model
		counter += 60
		model_name = 'neural_network_model_%dthsnd.h5' % (counter)
		nn.model.save(model_name)