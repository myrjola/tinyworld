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


########### The ViewController #######################

class ViewController:
    def __init__(self, mediator, container):
        self.mediator = mediator
        mediator.addObserver('tickwaiters', self)
        self.container = container
        self.container.screen = pygame.display.set_mode([1024,768])
        self.container.badGuysSprites = pygame.sprite.RenderUpdates()
        self.container.goodGuysSprites = pygame.sprite.RenderUpdates()
        self.container.background = pygame.Surface([1024, 768])
        self.container.background.fill([255,255,255])
        self.container.screen.blit(self.container.background, [0,0])
        pygame.display.flip()
        mediator.inform('levelcontrol', DisplayReady())
            
        
    def inform(self, event):
        if event.name == 'Tick':
            if event.tickname == 'InGameTick':
                '''
                Game running --> Draw movement
                '''
                self.container.badGuysSprites.update()
                self.container.goodGuysSprites.update()
                rectlist = self.container.badGuysSprites.draw(self.container.screen) +\
                        self.container.goodGuysSprites.draw(self.container.screen)
                pygame.display.update(rectlist)
                self.container.badGuysSprites.clear(self.container.screen, \
                        self.container.background)
                self.container.goodGuysSprites.clear(self.container.screen, \
                        self.container.background)
            elif event.tickname == 'MenuTick':
                '''
                Menu onscreen --> Draw menu
                '''
                print 'still to be done'    #TODO: draw menu


