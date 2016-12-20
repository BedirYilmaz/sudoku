import pygame, math, sys, time, random, snumber
from pygame.locals import *

class Snumber:
	'Common base class for all sudoku numbers'

	def __init__(self, posx, posy, value, rect):
		self.value = value
		self.posx = posx
		self.posy = posy
		self.Rect = rect
		self.status = False

	def getX(self):
		return self.posx

	def getY(self):
		return self.posy

	def getRect(self):
		return self.Rect

	def setValue(self, value):
		self.value = value

	def getValue(self):
		return self.value

	def toggleStatus(self):
		self.status = not (self.status)

	def getStatus(self):
		return self.status
