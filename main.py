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

import mvc

def main():
    #Hopefully starts the game
    pygame.init()
    mediator = mvc.Mediator()
    container = mvc.Container(mediator)
    keybd = mvc.KeyboardController(mediator)
    ticker = mvc.CPUController(mediator)
    levelcontrol = mvc.LevelController(mediator, container)
    viewcontrol = mvc.ViewController(mediator, container)
    collisioncontrol = mvc.CollisionController(mediator, container)
    ticker.tickTock() # starts the while loop

if __name__ == '__main__':
    main()

