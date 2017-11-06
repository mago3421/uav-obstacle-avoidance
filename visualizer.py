"""
Name: Visualizer Qt OpenGL Widget

Project: UAV Obstacle Avoidance Using Q-Learning Techniques

Authors: Katherine Glasheen, Marc Gonzalez, Shayon Gupta, 
Travis Hainsworth, Ramya Kanlapuli
	
Description: This class implements a PyQt widget used to draw
and animate all objects in the simulation.
"""

from OpenGL.GL import *
from PyQt5 import QtGui
from PyQt5.QtOpenGL import *
import math

class visualizer(QGLWidget):
	# Function to initialize grid with default 10 x 10 size
	def __init__(self, parent, entities, grid_width=10, grid_height=10):
		QGLWidget.__init__(self, parent)
		self.resize(800, 800)
		self.grid_width = 10
		self.grid_height = 10
		self.entities = entities

	# Function to initialize OpenGL state machine
	def initializeGL(self):	
		glClearColor(0, 0, 0, 0)              
		self.project()
		
	# Function called to render the scene
	def paintGL(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()
		# Draw grid (NOTE: May include this in entities too or add function to update grid)
		self.draw_grid()
		# Draw goal in red
		self.draw_text(self.entities["goal"].get_location(), "GOAL", [1, 0, 0])
		# Draw static obstacles
		for obstacle in self.entities["static"]:
			self.draw_obstacle(obstacle.get_location())
		# Draw dynamic obstacles in blue
		self.draw_uav(self.entities["dynamic"].get_location(), [0, 0, 1])
		# Draw agent in orange
		self.draw_uav(self.entities["agent"].get_location(), [1, 0.5, 0])
		# Render the scene
		glFlush()
	
	# Function called when widget is resized
	def resizeGL(self, width, height):
		# Paint within the whole window
		glViewport(0, 0, width, height)
		# Reproject view
		self.project()
	
	# Function called to set projection matrix
	def project(self):
		#  Select the projection matrix to manipulate
		glMatrixMode(GL_PROJECTION)
		#  Undo previous transformations
		glLoadIdentity()
		#  Multiply projection matrix by orthographic projection
		glOrtho(0, self.width(), 0, self.height(), -1, 1)
		#  Switch to manipulating the ModelView matrix again 
		glMatrixMode(GL_MODELVIEW)
		#  Undo previous transformations
		glLoadIdentity()
		
	# Update objects in 
	def update(self, entities):
		self.entities = entities if entities else self.entities
		self.project()
		self.updateGL()
		
	# Function to draw the static grid lines
	def draw_grid(self):
		# Get spacing for grids
		grid_width = self.width()/self.grid_width
		grid_height = self.height()/self.grid_height
		# Draw vertical lines
		for w in range(self.grid_width+1):
			# Save transformation
			glPushMatrix()
			# Draw lines
			glBegin(GL_LINE_STRIP)
			# Select white color
			glColor3f(1.0, 1.0, 1.0)
			glVertex2f(w * grid_width, 0)
			glVertex2f(w * grid_width, self.height())
			glEnd()
			glPopMatrix()
		# Draw horizontal lines
		for h in range(self.grid_height+1):
			# Save transformation
			glPushMatrix()
			# Draw lines
			glBegin(GL_LINE_STRIP)
			# Select white color
			glColor3f(1.0, 1.0, 1.0)
			glVertex2f(0, h * grid_height)
			glVertex2f(self.width(), h * grid_height)
			glEnd()
			# Pop projection matrix
			glPopMatrix()

	def draw_text(self, location, text, color):
		# Get spacing for grids
		grid_width = self.width()/self.grid_width
		grid_height = self.height()/self.grid_height
		# Get screen coordinates (These values were chosen visually)
		x = (location[0] * grid_width) + (0.25 * grid_width)
		y = (location[1] * grid_height) + (0.4 * grid_height)
		# Save transformation
		glPushMatrix()
		# Select text color
		glColor3f(color[0], color[1], color[2])		
		# Render text using Qt
		self.renderText(x, y, 0, text)
		# Pop projection matrix
		glPopMatrix()

	# Function to draw static obstacles as white squares
	def draw_obstacle(self, location):
		# Get spacing for grids
		grid_width = self.width()/self.grid_width
		grid_height = self.height()/self.grid_height
		# Get screen coordinates
		x = (location[0] * grid_width) + (0.5 * grid_width)
		y = (location[1] * grid_height) + (0.5 * grid_height)
		# Save transformation
		glPushMatrix()
		# Draw obstacles as white
		glColor3f(1.0, 1.0, 1.0)
		# Increase point size so one point occupies grid space
		glPointSize(grid_width)
		# Translate drawing to location on grid
		glTranslated(x, y, 0)
		# Draw point at center of square
		glBegin(GL_POINTS)
		glVertex2f(0, 0)
		glEnd()
		# Pop projection matrix
		glPopMatrix()
	
	# Function to draw uav with inputted location and color
	def draw_uav(self, location, color):
		# Get spacing for grids
		grid_width = self.width()/self.grid_width
		grid_height = self.height()/self.grid_height
		# Get screen coordinates
		x = (location[0] * grid_width) + (0.5 * grid_width)
		y = (location[1] * grid_height) + (0.5 * grid_height)
		# Save transformation
		glPushMatrix()
		# Choose color to draw uav
		glColor3f(color[0], color[1], color[2])
		# Translate drawing to location on grid
		glTranslated(x, y, 0)
		# Scale drawing to fit grid size
		glScaled(grid_width, grid_height, 1)
		# Enlarge points to serve as rotors
		glPointSize((grid_width)/4)
		# Draw top-left rotor
		glBegin(GL_POINTS)
		glVertex2f(-0.25, -0.25)
		glEnd()
		# Draw top-right rotor
		glBegin(GL_POINTS)
		glVertex2f(0.25, 0.25)
		glEnd()
		# Draw bottom-left rotor
		glBegin(GL_POINTS)
		glVertex2f(-0.25, 0.25)
		glEnd()
		# Draw bottom-right rotor
		glBegin(GL_POINTS)
		glVertex2f(0.25, -0.25)
		glEnd()
		# Enlarge line width
		glLineWidth(grid_height/32)
		# Draw body frame as an X
		glBegin(GL_LINE_STRIP)
		glVertex2f(-0.25, -0.25)
		glVertex2f(0.25, 0.25)
		glEnd()
		glBegin(GL_LINE_STRIP)
		glVertex2f(0.25, -0.25)
		glVertex2f(-0.25, 0.25)
		glEnd()
		# Pop projection matrix
		glPopMatrix()
		
		
	
