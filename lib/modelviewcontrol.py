############################################
# modelviewcontrol.py
# Author: Martin Yrjola
# An implementation of the design pattern
# model-view-controller using mediators.
############################################

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

# some important global variables
'''global walls
walls = []
global MAINCHARALIVE
MAINCHARALIVE = 1
'''
global walls
walls = []
########### The Mediator ###################

class Mediator:
    '''
    A base class to send events to other
    objects.

    '''
    def __init__(self):
        self.observers = []
        self.event_queue  = []
    def addObserver(self, observer):
        self.observers.append(observer)
    def delObserver(self, observer):
        self.observers.remove(observer)
        del(observer)
    def inform(self, event):
        # Sends an event to all observers
        for observer in self.observers:
            observer.inform(event)

########### Container ######################

class Container:
    ''' 
    Contains information needed by many
    game objects in the middle of the
    game ie. list of walls for collision-
    detection, time taken for one frame,
    etc...
    '''
    def __init__(self, mediator):
        self.mediator = mediator
        self.mediator.addObserver(self)
        self.solidwalls = []    # used for collision detection
        self.screen = 0
        self.background = 0     # the background-image and platforms reside here
        self.badGuysSprites = 0     # the enemies
        self.goodGuysSprites = 0    # the friends
        self.mainchar = 0           # hmm... what could this be
        self.maincharalive = 0 

    def inform(self, event):
        # still nothing implemented, maybe in the future...
        pass


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

class CPUController:
    '''
    The while-loop is here

    Implements fps-limit and takes care of gamepauses
    used with menus, inventories, dialogues etc.
    '''
    def __init__(self, mediator):
        self.mediator = mediator
        self.mediator.addObserver(self)
        self.clock = pygame.time.Clock()
        self.ticking = 1
        self.state = "ingame"
        self.ticktime = 0
    def tickTock(self):
        while self.ticking:
            self.clock.tick(35)
            if self.state == "ingame":
                self.mediator.inform(InGameTick())
            elif self.state == "menu":
                self.mediator.inform(MenuTick())
            elif self.state == "pause":
                self.mediator.inform(PauseTick())
    def inform(self, event):
        if event.name == 'Quit':
            # stop the while-loop
            self.ticking = 0

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
           
########### The ViewController #######################

class ViewController:
    def __init__(self, mediator, container):
        self.mediator = mediator
        mediator.addObserver(self)
        self.container = container
        self.container.screen = pygame.display.set_mode([1024,768])
        self.container.badGuysSprites = pygame.sprite.RenderUpdates()
        self.container.goodGuysSprites = pygame.sprite.RenderUpdates()
        self.container.background = pygame.Surface([1024, 768])
        self.container.background.fill([255,255,255])
        self.container.screen.blit(self.container.background, [0,0])
        pygame.display.flip()
        mediator.inform(DisplayReady())
            
        
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


