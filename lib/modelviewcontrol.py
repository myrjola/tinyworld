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

from gamefunc import *
from gameinstances import *

# some important global variables
'''global walls
walls = []
global MAINCHARALIVE
MAINCHARALIVE = 1
'''

########### The Events #####################

class Tick:
    def __init__(self):
        self.name = "Tick"

class InGameTick(Tick):
    def __init__(self):
        Tick.__init__(self)
        self.tickname = "InGameTick"

class MenuTick(Tick):
    def __init__(self):
        Tick.__init__(self)
        self.tickname = "MenuTick"

class PauseTick(Tick):
    def __init__(self):
        self.tickname = "PauseTick"

class Quit:
    def __init__(self):
        self.name = "Quit"

class MoveChar:
    def __init__(self, direction):
        self.name = "MoveChar"
        self.direction = direction 

class DisplayReady:
    def __init__(self):
        self.name = "DisplayReady"

class LevelChange:
    def __init__(self, x, y):
        self.name = "LevelChange"
        self.left_or_right = x
        self.up_or_down = y

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
        print "mediator has been informed of event" + event.name
        for observer in self.observers:
            print self.observers
            print " has been informed of " + event.name
            observer.inform(event)

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
                    print "Quit"

                elif input_event.type == KEYDOWN:
                    if input_event.key == K_ESCAPE:
                        ev = Quit()
                        print "Quit"

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
                print ev            
                if ev:
                    print ev.name
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
    def tickTock(self):
        while self.ticking:
            self.clock.tick(30)
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
    def __init__(self,mediator):
        self.mediator = mediator
        self.mediator.addObserver(self)
        self.curlevel = [0,0]
        
    def inform(self, event):
        if event.name == 'DisplayReady':
            mediator = self.mediator
            self.CreateLevel(self.OpenLevelFile('00'))
        if isinstance(event, LevelChange):
            self.curlevel[0] += event.left_or_right
            self.curlevel[1] += event.up_or_down
            self.CreateLevel(self.OpenLevelFile(str(self.curlevel[0]) +\
                    str(self.curlevel[1])))



    def CreateLevel(self,level):
        mediator = self.mediator
        background.fill([255,255,255])
        badGuysSprites.empty()
        '''
        if MAINCHARALIVE:
            mainchar.rect.topleft = [33,33]            
            goodGuysSprites.add(mainchar)
        '''
        walls = []
        for i in level["mainchar"]:
            global mainchar
            mainchar = MainChar(self.mediator,i)
        for i in level["badguys"]:
            badGuysSprites.add(badGuy(mediator, i))
        for i in level["balls"]:
            badGuysSprites.add(bouncyBall(mediator, i))
        for i in level["platforms"]:
            background.blit(solidPlatform(i).image,i)
        for i in level["walls"]:
            background.blit(solidWall(i).image,i)
        screen.blit(background,(0,0))
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

    def __init__(self, mediator):
        self.mediator = mediator
        self.mediator.addObserver(self)

    def inform(self, event):
        if event.name == 'Tick':
            collisions = pygame.sprite.groupcollide(goodGuysSprites, 
                    badGuysSprites, False, False) #returns dictionary
            for smashed in collisions: #"smashed"key returns collisionlist
                for colobj in collisions[smashed]:
                    print smashed, "collided with", colobj
                    colobj.Collide(smashed) #badguy collision event 
                    smashed.Collide(colobj) #goodguy collision event
           
########### The ViewController #######################

class ViewController:
    def __init__(self,mediator):
        self.mediator = mediator
        mediator.addObserver(self)
        #global screen
        screen = pygame.display.set_mode([1024,768])
        global badGuysSprites
        badGuysSprites = pygame.sprite.RenderUpdates()
        global goodGuysSprites
        goodGuysSprites = pygame.sprite.RenderUpdates()
        global background
        background = pygame.Surface([1024, 768])
        background.fill([255,255,255])
        screen.blit(background, [0,0])
        pygame.display.flip()
        mediator.inform(DisplayReady())
            
        
    def inform(self, event):
        if event.name == 'Tick':
            if event.tickname == 'InGameTick':
                '''
                Game running --> Draw movement
                '''
                badGuysSprites.update()
                goodGuysSprites.update()
                rectlist = badGuysSprites.draw(screen) + \
                        goodGuysSprites.draw(screen)
                pygame.display.update(rectlist)
                badGuysSprites.clear(screen, background)
                goodGuysSprites.clear(screen, background)
            elif event.tickname == 'MenuTick':
                '''
                Menu onscreen --> Draw menu
                '''
                print 'still to be done'    #TODO: draw menu



