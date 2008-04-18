#!/usr/bin/python

########################################
#main.py
#This is a simple platformer game test
#I'm trying to learn pygame and python
#let's hope it's going to be playable
########################################

import math, os, sys, pygame
from pygame.locals import *

#makes importing of modules in lib directory possible
sys.path.insert(0, os.path.join("lib")) 
from MVC import *
#from objects import *
from gamefunc import *


if __name__ == '__main__':
	#Hopefully starts the game
	pygame.init()
	evManager = EventManager()
	keybd = KeyboardController( evManager)
	spinner = CPUSpinnerController(evManager)
	pygameView = PygameView(evManager)
	
	evManager.RegisterListener(keybd)
	evManager.RegisterListener(spinner)
	evManager.RegisterListener(pygameView)

	spinner.Run()

