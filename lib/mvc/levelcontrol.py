
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
        self.mediator.addObserver('levelcontrol', self)
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
        self.container.background.fill([255,255,255])
        self.container.badGuysSprites.empty()
        self.container.solidwalls = []
        for objname, datalist in level.iteritems():
            if objname == 'MainChar':
                self.container.mainchar = MainChar(self.mediator,\
                        self.container, datalist[0][0])
                self.container.goodGuysSprites.add(self.container.mainchar)
                self.container.maincharalive = 1
            elif objname.find('solid') != -1: # the object is a platform
                for i in datalist:
                    globals()[objname](self.container, i[0])
            else:
                for i in datalist:
                    self.container.badGuysSprites.add(globals()[objname](self.mediator, \
                            self.container, i[0])) 
        pygame.display.get_surface().blit(self.container.background,(0,0))
        pygame.display.flip()


    def OpenLevelFile(self,file):
        fullname = os.path.join('levels',file)
        levelfile = open(fullname, 'r')
        leveldata = pickle.load(levelfile)
        return leveldata


