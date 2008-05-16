#!/usr/bin/python

########################################
#main2.py
#This is a simple platformer game test
#I'm trying to learn pygame and python
#let's hope it's going to be playable
########################################

import math
import os
import sys

import pygame
from pygame.locals import *

#makes importing of modules in lib directory possible
sys.path.insert(0, os.path.join("lib")) 

from gameinstances import *
from gamefunc import *

global walls
walls = []
global screen

def main():
    #Hopefully starts the game
    pygame.init()
    mediator = Mediator()
    keybd = KeyboardController(mediator)
    ticker = CPUController(mediator)
    levelcontrol = LevelController(mediator)
    viewcontrol = ViewController(mediator)
    collisioncontrol = CollisionController(mediator)
    # starts the while loop
    ticker.tickTock()

if __name__ == '__main__':
    main()

