
import math
import os
import sys
import pickle
import random

import pygame
from pygame.locals import *

# makes importing of modules in lib directory possible
sys.path.insert(0, os.path.join("lib")) 

from gameinstances import *
from gamefunc import *
from events import *


class CollisionController:
    '''
    Handles collisionmanagement
    '''

    def __init__(self, mediator, container):
        self.mediator = mediator
        self.mediator.addObserver(self)
        self.container = container

    def inform(self, event):
        if event.name == 'Tick':
            if event.tickname == 'InGameTick':
                collisions = pygame.sprite.groupcollide(self.container.goodGuysSprites, 
                        self.container.badGuysSprites, False, False) #returns dictionary
                for smashed in collisions: #"smashed"key returns collisionlist
                    for colobj in collisions[smashed]:
                        print smashed, "collided with", colobj
                        colobj.Collide(smashed) #badguy collision event 
                        smashed.Collide(colobj) #goodguy collision event
 
