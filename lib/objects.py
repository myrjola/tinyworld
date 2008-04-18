##########################
#objects.py
#class library including charactors
#and other misc objects for a platformer
###########################

import math, os, sys, pygame
from pygame.locals import *

#makes importing of modules in lib directory possible
sys.path.insert(0, os.path.join("lib")) 
from MVC import *
from gamefunc import *
from main import *





class mainChar(pygame.sprite.Sprite):
	"""The main character of the game
	"""
	image = None

	def __init__(self, evManager, startLocation):
		pygame.sprite.Sprite.__init__(self)
		self.evManager = evManager
		self.evManager.RegisterListener(self)
		if mainChar.image == None:
			mainChar.image, mainChar.rect = load_png('char1.png')

		self.image = mainChar.image
		self.rect = self.image.get_rect()
		screen = pygame.display.get_surface()
		self.rect.topleft = startLocation

	def Update(self):
		self.rect = newpos
	
	def Move(self, direction):
		self.newpos =  self.rect
		if direction == "jump":
			#TODO: make character jump
			return
		elif direction == "left":
			#TODO
			newpos.move(5,0)
		elif direction == "right":
			#TODO
			newpos.move(-5,0)
		elif direction == "duck":
			#TODO: make character duck, could be tricky as hell
			return

	def Notify(self, event):
		if isinstance(event, CharMoveRequest):
			self.Move(event.direction)



class bounceBall(pygame.sprite.Sprite):
	"""A ball that bounces around the screen
	"""
	image = None
	
	def __init__(self, vector, startLocation):
		pygame.sprite.Sprite.__init__(self)
		#self.evManager = evManager
		#self.evManager.RegisterListener( self )

		if bounceBall.image is None:
			bounceBall.image, bounceBall.rect = load_png('ball1.png')
			
		self.image = bounceBall.image
		self.rect = self.image.get_rect()
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.vector = vector
		self.rect.topleft = startLocation
	def update(self):
		newpos = self.calcnewpos(self.rect,self.vector)
		self.rect = newpos
		#Make ball bounce from windowborders
		(angle,z) = self.vector
		if not self.area.contains(newpos):
			from math import pi
			tl = not self.area.collidepoint(newpos.topleft)
			tr = not self.area.collidepoint(newpos.topright)
			bl = not self.area.collidepoint(newpos.bottomleft)
			br = not self.area.collidepoint(newpos.bottomright)
			if tr and tl or (br and bl):
				angle = -angle
			if tl and bl:
				angle = pi - angle
			if tr and br:
				angle = pi - angle
		self.vector = (angle,z)
		

	def calcnewpos(self,rect,vector):
		(angle,z) = vector
		(dx, dy) = (z*math.cos(angle), z*math.sin(angle))
		return rect.move(dx,dy)

#class Background(pygame.Surface):
#	def __init__(self):
		

class mainChar1(pygame.sprite.Sprite):
	"""The main character of the game
	This is a test with another type of control without
	incorporating MVC and a mediator
	"""
	image = None

	def __init__(self, startLocation):
		pygame.sprite.Sprite.__init__(self)
		if mainChar.image == None:
			mainChar.image, mainChar.rect = load_png('char1.png')

		self.image = mainChar.image
		self.rect = self.image.get_rect()
		screen = pygame.display.get_surface()
		self.rect.topleft = startLocation
		self.movepos = (0,0)

	def update(self):
		self.rect.move(self.movepos) 

	def Move(self, direction):
		if direction == "jump":
			self.movepos = (0,-5)
			#TODO: make character jump
		elif direction == "left":
			self.movepos = (5,0)
			#TODO
		elif direction == "right":
			self.movepos = (-5,0)
			#TODO
		elif direction == "duck":
			#TODO: make character duck, could be tricky as hell
			self.movepos = (0,5)
		else: self.movepos = (0,0)




