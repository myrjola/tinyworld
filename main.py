#!/usr/bin/python

##################################33
#main.py
#This is a simple platformer game test
#I'm trying to learn pygame and python
#We'll hope this is going to be playable
########################################
def Debug(msg):
	print msg

import math, os, sys, pygame
from pygame.locals import *

pygame.init()

sys.path.insert(0, os.path.join("lib")) 
#makes importing of modules in lib directory possible


def main():
	evManager = EventManager()
	keybd = KeyboardController()
	spinner = CPUSpinnerController()
	pygameView = PygameView()
	
	evManager.RegisterListener( keybd)
	evManager.RegisterListener( spinner)
	evManager.RegisterListener(pygameView)

	spinner.Run()

if __name__ == '__main__':
	main()
