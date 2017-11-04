
import argparse
import numpy as np
from collections import Counter, defaultdict
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import Dense
from keras.layers import MaxPool2D
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.core import Reshape
from keras.utils import np_utils

def Generate_Training_Data(Agent=None, Num_Games = 10000, Saved_Games_Percentage = 0.1):
    '''
    Generates data based on a inputted agent, or generates training data based on a random agent

    Agent takes in a position and outputs an action
    '''

    if Agent == None:
        # TODO implement random agent
        pass

    # Make the dictionary of succesfull game states where the key is the length of the policy that was found
    Game_List = 0 # TODO

    for i in range(Num_Games):
        # Create empty lists to store game data
        action_sequence = [] # Each addition should be a single value
        position_sequence = [] # Each addition shoulb be 2 values (x,y)
        reward_sequence = []  # Each addition should be 5 values (R_left, R_right, R_up, R_down, R_stay) where R is the reward viewed when anticipating that action

        # Initialize game instance
        # TODO start game
        # This will be done by calling the simulation which creates environments and agents
        position = 0 # TODO

        # Play game until you reach a terminal state
        while position is not terminal_state: #TODO implement from game environment
            action = Agent(position) # TODO
            position = 0 # TODO
            rewards = 0 # TODO

            action_sequence.append(action)
            position_sequence.append(position)
            reward_sequence.append(rewards)

        # Only store the game if you made it to the goal and did not crash into an obstacle
        if position == goal: # TODO - get goal state from game environment
            game_history = [action_sequence, position_sequence, reward_sequence]
            Game_List.append(game_history, len(position_sequence)) # TODO - wrong syntax for dictionary
            
    # Sort the game list by policy length
    # Todo
    # Save only the shortest policy games
    # Todo
            
    pass


class NN:
    '''
    NN classifier
    '''
    def __init__(self, train_x, train_y, test_x, test_y, epoches = 15, batch_size=63):
        '''
        initialize NN classifier
        '''
        self.batch_size = batch_size
        self.epoches = epoches


        # TODO: one hot encoding for train_y and test_y

        # TODO: build model
        self.model = Sequential()
        
        self.model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

    def train(self):
        '''
        train NN classifier with training data
        :param x: training data input
        :param y: training label input
        :return:
        '''
        # TODO: fit in training data    
        EarlyStoppingVar = keras.callbacks.EarlyStopping('val_loss')    
        self.model.fit(self.train_x, self.train_y, self.batch_size, self.epoches, verbose=1, callbacks=[EarlyStoppingVar],validation_split=0.1,shuffle=True)

    def evaluate(self):
        '''
        test NN classifier and get accuracy
        :return: accuracy
        '''
        acc = self.model.evaluate(self.test_x, self.test_y)
        return acc

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CNN classifier options')
    parser.add_argument('--limit', type=int, default=-1,
                        help='Restrict training to this many examples')
    args = parser.parse_args()

    # Todo make training data

    # Todo sort data from position, reward, action to an input and output data set

    nn = NN(data.train_x[:args.limit], data.train_y[:args.limit], data.test_x, data.test_y)
    nn.train()
    acc = nn.evaluate()
    print(acc)

    # TOdo use the new agent on a world