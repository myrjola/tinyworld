#!/usr/bin/python

########################################
# main2.py
# This is a simple platformer game test
# I'm trying to learn pygame and python
# let's hope it's going to be playable
########################################

import math
import os
import sys

import pygame
from pygame.locals import *

#makes importing of modules in lib directory possible
sys.path.insert(0, os.path.join("lib")) 

import gameinstances
import modelviewcontrol

def main():
    #Hopefully starts the game
    pygame.init()
    mediator = modelviewcontrol.Mediator()
    container = modelviewcontrol.Container(mediator)
    keybd = modelviewcontrol.KeyboardController(mediator)
    ticker = modelviewcontrol.CPUController(mediator)
    levelcontrol = modelviewcontrol.LevelController(mediator, container)
    viewcontrol = modelviewcontrol.ViewController(mediator, container)
    collisioncontrol = modelviewcontrol.CollisionController(mediator, container)
    # starts the while loop
    ticker.tickTock()

if __name__ == '__main__':
    main()

