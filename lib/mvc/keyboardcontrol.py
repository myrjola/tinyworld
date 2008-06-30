
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

########### The Controllers ################

class KeyboardController:
    '''
    Handles input events
    '''
    def __init__(self, mediator):
        self.mediator = mediator
        self.mediator.addObserver(self)
    def inform(self, event):
        if event.name == 'Tick':

            for input_event in pygame.event.get():
                ev = None
                if input_event.type == QUIT:
                    ev = Quit()

                elif input_event.type == KEYDOWN:
                    if input_event.key == K_ESCAPE:
                        ev = Quit()

                if event.tickname == 'InGameTick':
                    # Movement of character possible

                    if input_event.type == KEYDOWN:
                        if input_event.key == K_UP:
                            ev = MoveChar('jump')
                        elif input_event.key == K_DOWN:
                            ev = MoveChar('duck')
                        elif input_event.key == K_LEFT:
                            ev = MoveChar('left')
                        elif input_event.key == K_RIGHT:
                            ev = MoveChar('right')
                        pygame.event.pump()
                    
                    elif input_event.type == KEYUP:
                        keys = pygame.key.get_pressed()
                        if not 1 in [keys[K_LEFT], keys[K_RIGHT]]:
                            ev = MoveChar('stophorisontalmovement')
                if ev:
                    self.mediator.inform(ev)

