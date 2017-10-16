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
	def __init__(self, parent, height=10, width=10):
		QGLWidget.__init__(self, parent)
		self.setMinimumSize(800, 800)
		self.height = height
		self.width = width

	def initializeGL(self):	
		glClearColor(0, 0, 0, 0)              
		self.project()
		
	# Function called to render the scene
	def paintGL(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()
		glFlush()
	
	# Function called to set projection matrix
	def project(self):
		#  Select the projection matrix to manipulate
		glMatrixMode(GL_PROJECTION)
		#  Undo previous transformations
		glLoadIdentity()
		#  Multiply projection matrix by orthographic projection
		#glOrtho()
		#  Switch to manipulating the ModelView matrix again 
		glMatrixMode(GL_MODELVIEW)
		#  Undo previous transformations
		glLoadIdentity()
		
	# Update objects in 
	def update(self, entities):
		self.entities = entities if entities else self.entities
		self.reproject()
		self.updateGL()
		
	# Function called when the screen is reprojected
	def reproject(self):
		# Select projection matrix
		glMatrixMode(GL_PROJECTION)
		# Undo previous transformations
		glLoadIdentity()
		#glOrtho(self.minLon, self.maxLon, self.minLat, self.maxLat, -1, 1)
		glMatrixMode(GL_MODELVIEW)
		# Undo previous transformations
		glLoadIdentity()
		
	
