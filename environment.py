"""
Name: Environment Qt Application

Project: UAV Obstacle Avoidance Using Q-Learning Techniques

Authors: Katherine Glasheen, Marc Gonzalez, Shayon Gupta, 
Travis Hainsworth, Ramya Kanlapuli
	
Description: This class implements a PyQt widget used to draw
and animate all objects in the simulation.
"""

from pyqtgraph.Qt import QtGui, QtCore
from copy import *
from visualizer import *
from entity import *
from uav import *
#from agent import *

class environment(QtGui.QWidget):
	# Function to initialize environment
	def __init__(self, entities):
		# Start app and create main window
		self.app = QtGui.QApplication([])
		self.main_window = QtGui.QMainWindow()
		QtGui.QWidget.__init__(self)
		self.entities = entities
		
	# Function to create window
	def create_window(self):
		# Create window, set title, and set central widget
		self.main_window.setWindowTitle('UAV Obstacle Avoidance Simulation')
		self.main_window.resize(1000, 900)
		self.main_window.setCentralWidget(self)
		# Create grid layout for which to add widgets
		self.layout = QtGui.QGridLayout()
		self.setLayout(self.layout)		
		# Create widgets and add to layout
		self.create_widgets()
		# Show the window
		self.main_window.show()
		# Run the app
		self.app.exec_()
		
	# Function to add each widget to window
	def create_widgets(self):
		# Create simulation graphics
		self.create_visualizer()
		# Create control panels with buttons
		self.create_control_panel()

	# Function to create buttons on control panel
	def create_control_panel(self):
		# Create reset button
		reset_button = QtGui.QPushButton('Reset')
		reset_button.clicked.connect(self.reset_simulation)
		reset_button.setMaximumSize(100, 50)
		reset_button.setMinimumSize(100, 50)
		self.layout.addWidget(reset_button, 0, 800)
		# Create step button
		step_button = QtGui.QPushButton('Step')
		step_button.clicked.connect(self.step_simulation)
		step_button.setMaximumSize(100, 50)
		step_button.setMinimumSize(100, 50)
		self.layout.addWidget(step_button, 100, 800)
		# Create reverse button
		reverse_button = QtGui.QPushButton('Reverse')
		reverse_button.clicked.connect(self.reverse_simulation)
		reverse_button.setMaximumSize(100, 50)
		reverse_button.setMinimumSize(100, 50)
		self.layout.addWidget(reverse_button, 100, 800)
		
	# Function to create visualizer widget and add to layout
	def create_visualizer(self):
		# Pass main window so the visualizer can access objects in environment
		self.visualizer = visualizer(self.main_window)
		# Place visualizer at origin
		self.layout.addWidget(self.visualizer, 0, 0)
		
	# Function to update window upon button click or time step
	def update_window(self):
			# Send copy so as not to entangle with self.entities (May be bad practice; unsure)
			self.view(deepcopy(self.entities))
			
	# Function to reset all objects to their original state (Not sure about the model however)
	def reset_simulation(self):
		#TODO: Reset self.entities to original object state from file or saved state
		pass
		
	# Function to step forward in simulation
	def step_simulation(self):
		#TODO: Step objects in self.entities forward in simulation
		pass
		
	# Function to go back a step in simulation
	def reverse_simulation(self):
		#TODO: Revert self.entities to previous state
		pass
		
	def run(self):
		self.create_window()
		
# Unit Test
if __name__ == "__main__":
	env = environment([])
	env.run()
	
		
	
