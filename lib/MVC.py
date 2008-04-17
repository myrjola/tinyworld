#######################
#MVC.py
#My first try to implement a Model-View-Controller
#Many thing stolen from sjbrowns tutorial
###################3

import math, os, sys, pygame
from pygame.locals import *

#makes importing of modules in lib directory possible
sys.path.insert(0, os.path.join("lib")) 
from MVC import *
from objects import *
from gamefunc import *
from main import *



class Event:
	"""event superclass"""
	def __init__(self):
		self.name = "Generic Event"

class TickEvent(Event):
	def __init__(self):
		self.name = "CPU Tick Event"

class QuitEvent(Event):
	def __init__(self):
		self.name = "Program Quit Event"
class GameStartedEvent(Event):
	def __init__(self, game):
		self.name = "Game Started Event"
		self.game = game
class CharactorMoveRequest(Event):
	def __init__(self, charactor):
		self.name = "Charactor Move Event"
		self.direction = direction

class EventManager:
	"""The mediator betveen MVC"""
	def __init__(self):
		from weakref import WeakKeyDictionary
		self.listeners = WeakKeyDictionary()
		self.eventQueue = []

	def RegisterListener(self, listener):
		self.listeners[ listener ] = 1
	
	def UnregisterListener(self, listener):
		if listener in self.listeners.keys():
			del self.listeners[ listener ]
	
	def Post(self, event):
		for listener in self.listeners.keys():
			#NOTE: If the weakref has died it will
			#be automatically removed, so we don't
			#have to worry about it
			listener.Notify(event)
	
	def Notify(self, event):
		for listener in self.listeners.keys():
			#If weakref has died, remove it and continue
			#through the list
			if listener is None:
				del self.listeners[listener]
				continue
			listener.Notify(event)


class KeyboardController:
	def __init__(self,evManager):
		self.evManager = evManager
		self.evManager.RegisterListener(self)
	def Notify(self, event):
		if isinstance( event, TickEvent ):
			#TODO: Handle input events
			for event in pygame.event.get():
				ev = None
				if event.type == QUIT:
					ev = QuitEvent()
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						ev = QuitEvent()
					elif event.key == K_UP:
						ev = CharactorMoveRequest('jump')
					elif event.key == K_DOWN:
						ev = CharactorMoveRequest('duck')
					elif event.key == K_LEFT:
						ev = CharactorMoveRequest('left')
					elif event.key == K_UP:
						ev = CharactorMoveRequest('right')
				if ev:
					self.evManager.Notify( ev )
	
	


class CPUSpinnerController:
	def __init__(self,evManager):
		#implement fps-limit
		self.clock = pygame.time.Clock()
		self.evManager = evManager
		self.keepGoing = 1

	def Run(self):
		while self.keepGoing:
			self.clock.tick(30)
			event = TickEvent()
			self.evManager.Notify(event)

	def Notify(self,event):
		if isinstance(event,QuitEvent):
			#stop the while loop
			self.keepGoing = 0

class PygameView:
	def __init__(self,evManager):
		self.evManager = evManager
		evManager.RegisterListener( self )
		self.screen = pygame.display.set_mode([800,400])
		self.spritegroup = pygame.sprite.RenderUpdates()
		self.spritegroup.add(bounceBall(evManager, (1,5), [400,200]))
		self.background = pygame.Surface([800, 400])
		self.background.fill([255,255,255])
		self.screen.blit(self.background, [0,0])
		pygame.display.flip()
			
		
	def Notify(self, event):
		if isinstance( event, TickEvent ):
			#TODO; draw everything
			self.spritegroup.update()
			rectlist = self.spritegroup.draw(self.screen)
			pygame.display.update(rectlist)
			self.spritegroup.clear(self.screen, self.background)

			


