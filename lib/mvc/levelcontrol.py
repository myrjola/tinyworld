
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

class LevelController:
    '''
    Handles the creation of levels and
    changes of levels.
    '''
    def __init__(self, mediator, container):
        self.mediator = mediator
        self.mediator.addObserver(self)
        self.container = container
        self.curlevel = [0,0]
        
    def inform(self, event):
        if event.name == 'DisplayReady':
            self.CreateLevel(self.OpenLevelFile('00'))
        if isinstance(event, LevelChange):
            print "self.curlevel= ", self.curlevel
            self.curlevel[0] += event.left_or_right
            self.curlevel[1] += event.up_or_down
            print "self.curlevel= ", self.curlevel
            self.CreateLevel(self.OpenLevelFile(str(self.curlevel[0]) +\
                    str(self.curlevel[1])))



    def CreateLevel(self,level):
        # cleanup
        mediator = self.mediator
        self.container.background.fill([255,255,255])
        self.container.badGuysSprites.empty()
        self.container.solidwalls = []
        '''
        if MAINCHARALIVE:
            mainchar.rect.topleft = [33,33]            
            goodGuysSprites.add(mainchar)
        '''
        walls = []
        for i in level["mainchar"]:
            if not self.container.maincharalive:
                self.container.mainchar = MainChar(self.mediator, self.container, i) # init the mainchar
                self.container.goodGuysSprites.add(self.container.mainchar)
                self.container.maincharalive = 1
        for i in level["badguys"]:
            self.container.badGuysSprites.add(badGuy(mediator, self.container, i))
        for i in level["balls"]:
            self.container.badGuysSprites.add(bouncyBall(mediator, self.container, i))
        for i in level["platforms"]:
            platformrect = Rect(i, (96,32))
            self.container.solidwalls.append(platformrect)
            self.container.background.blit(solidPlatform(i).image,\
                    platformrect)
        for i in level["walls"]:
            wallrect = Rect(i, (32,64))
            self.container.solidwalls.append(wallrect)
            self.container.background.blit(solidWall(i).image,wallrect)
        pygame.display.get_surface().blit(self.container.background,(0,0))
        pygame.display.flip()


    def OpenLevelFile(self,file):
        fullname = os.path.join('levels',file)
        levelfile = open(fullname, 'r')
        leveldata = pickle.load(levelfile)
        return leveldata


