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

       
class badGuy(pygame.sprite.Sprite, phys.PlatformerPhysics):
    image = None
    def __init__(self,mediator, container, startLocation):
        pygame.sprite.Sprite.__init__(self)
        phys.PlatformerPhysics.__init__(self, container)
        self.mediator = mediator
        self.container = container
        if badGuy.image is None:
            badGuy.image, badGuy.rect = imgLoad('badguy1.png')

        self.image = badGuy.image
        self.imageright = self.image
        self.imageleft = pygame.transform.flip(self.imageright,True,False)
        self.rect = self.image.get_rect()
        self.area = self.container.screen.get_rect()
        self.rect.topleft = startLocation
        self.movepos = [0,0]
        self.jumpable = 0
        self.jumpabletimes = 1 
        self.speed = 5
        self.deadly = True
    
    def update(self):
        self.newpos = self.rect.move(self.movepos)
        phys.PlatformerPhysics.update(self)
        self.rect = self.newpos
        if not self.rect.colliderect(self.area):
            self.kill()
        #chase mainchar
        if self.container.mainchar.rect.centerx >= self.rect.right: 
            self.MoveRight(self.speed)
            self.image = self.imageright
        elif self.container.mainchar.rect.centerx <= self.rect.left:
            self.MoveLeft(-self.speed)
            self.image = self.imageleft
        else:
            self.StopMoving()

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
        if self.jumpable >= 1:
            self.jumpable -= 1
            self.movepos[1] = -2*self.speed
     

    def Collide(self, collideobject):
        print "bigouch!"

    def __del__(self):
        pass

