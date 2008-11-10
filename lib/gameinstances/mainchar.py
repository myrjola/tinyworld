import math
import os
import sys
import pickle
import random

import pygame
from pygame.locals import *

# makes importing of modules in lib directory possible
sys.path.insert(0, os.path.join("lib")) 

import phys
from events import *
from gamefunc import *


class MainChar(pygame.sprite.Sprite, phys.PlatformerPhysics):
    """The main character of the game
    """
    anidict = None

    def __init__(self, mediator, container, startLocation):
        pygame.sprite.Sprite.__init__(self)
        phys.PlatformerPhysics.__init__(self, container)
        self.mediator = mediator
        self.mediator.addObserver('inputwaiters', self)
        self.container = container
        if MainChar.anidict == None:
            MainChar.anidict = aniDictMake('mainchar', ['still', 'walk'],\
                    [4, 4])
        self.imagelist = MainChar.anidict['still_right']
        self.image = self.imagelist[0]
        self.rect = self.image.get_rect()
        self.startLocation = startLocation
        self.rect.topleft = startLocation
        self.area = self.container.screen.get_rect()
        self.speed = 9.0
        self.movepos = [0,0]
        self.jumpable = 1
        self.jumpabletimes = 2
        self.direction = 'right'
        self.state = "still"
        self.frame = 0
        self.frametick = 0

    def update(self):

        self.newpos = self.rect.move(self.movepos)
        
        phys.PlatformerPhysics.update(self)
        #levelchange
        if not self.rect.colliderect(self.area):
            levelcord = [0,0]
            if self.rect.right <= self.area.left:
                levelcord[0] = -1
                self.newpos.centerx = 1024
                self.newpos.centery -= 1 # to avoid falling through walls
            elif self.rect.left >= self.area.right:
                levelcord[0] = 1
                self.newpos.centerx = 0
                self.newpos.centery -= 1 # to avoid falling through walls
            elif self.rect.top >= self.area.bottom:
                levelcord[1] = 1
                self.newpos.centery = 0
            elif self.rect.bottom <= self.area.top:
                levelcord[1] = -1
                self.newpos.centery = 768
            self.startLocation = self.newpos.topleft
            self.rect = self.newpos # to avoid levelchange loop
            self.mediator.inform('levelcontrol', LevelChange(levelcord[0],\
                levelcord[1]))
        # animate the character
        self.imagelist = self.anidict[self.state + '_' + self.direction]
        try:
            self.image = self.imagelist[self.frame]
        except IndexError:
            self.frame = 0
            self.image = self.imagelist[self.frame]
        self.frametick += 1
        if self.frametick == 5:
            #self.frame += 1
            self.frametick = 0
        #move the character
        self.rect = self.newpos

    def StopMoving(self):
        self.movepos[0] = 0 

    def MoveLeft(self, speed): 
        newpos = self.rect.move(-1,self.movepos[1])
        if newpos.collidelist(self.container.solidwalls) == -1:
            self.movepos[0] = speed

    def MoveRight(self, speed):
        newpos = self.rect.move(1,self.movepos[1])
        if newpos.collidelist(self.container.solidwalls) == -1:
            self.movepos[0] = speed

    def Jump(self):
        newpos = self.rect.move(self.movepos[0],-1)
        if newpos.collidelist(self.container.solidwalls) == -1:
            if self.jumpable >= 1:
                self.jumpable -= 1
                self.movepos[1] = -2*self.speed
                 
    def Collide(self, collideobject):
        if collideobject.deadly == True:
            self.rect.topleft = self.startLocation
            pygame.time.delay(300)
        else:
            collideobject.kill()

    
    def inform(self, event):
        if event.name == 'MoveChar':
            self.move = event.direction
            self.state = "walk"
            if self.move == "left":
                self.direction = 'left'
                self.movepos[0] = -self.speed
                
            elif self.move == "right":
                self.direction = 'right'
                self.movepos[0] = self.speed
 
            elif self.move == "jump":
                self.Jump()
                   
            elif self.move == "stophorisontalmovement":
                self.state = "still"
                self.movepos[0] = 0
    
    def __del__(self):
        self.mediator.delObserver(self)


