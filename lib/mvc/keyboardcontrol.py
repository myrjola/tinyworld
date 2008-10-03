
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
        self.mediator.addObserver('tickwaiters', self)
    def inform(self, event):
        if event.name == 'Tick':

            for input_event in pygame.event.get():
                ev = None
                if input_event.type == QUIT:
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
                        elif input_event.key == K_p:
                            print "Pause"
                            ev = ChangeState('pause')
                        elif input_event.key == K_ESCAPE:
                            ev = ChangeState('menu')
                    
                    elif input_event.type == KEYUP:
                        keys = pygame.key.get_pressed()
                        if not 1 in [keys[K_LEFT], keys[K_RIGHT]]:
                            ev = MoveChar('stophorisontalmovement')

                elif event.tickname == 'MenuTick':
                    # Control the menu
                    if input_event.type == KEYDOWN:
                        if input_event.key == K_UP:
                            ev = MenuNav('up')
                        elif input_event.key == K_DOWN:
                            ev = MenuNav('down')
                        elif input_event.key == K_LEFT:
                            ev = MenuNav('back')
                        elif (input_event.key == K_RIGHT or\
                                input_event.key == K_RETURN):
                            ev = MenuNav('enter')
                        elif input_event.key == K_ESCAPE:
                            ev = ChangeState('ingame')
                     
                elif event.tickname == 'PauseTick':
                    if input_event.type == KEYDOWN:
                        ev = ChangeState('ingame')

                pygame.event.pump()

                if ev:
                    self.mediator.inform('inputwaiters', ev)


