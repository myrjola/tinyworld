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



class bounceBall(pygame.sprite.Sprite):
    """A ball that bounces around the screen
    """
    image = None
    
    def __init__(self, mediator, vector, startLocation):
        pygame.sprite.Sprite.__init__(self)
        self.mediator = mediator
        #self.mediator.addmediator( self )

        if bounceBall.image is None:
            bounceBall.image, bounceBall.rect = imgLoad('ball1.png')
            
        self.image = bounceBall.image
        self.rect = self.image.get_rect()
        self.area = screen.get_rect()
        self.vector = vector
        self.rect.topleft = startLocation
        self.deadly = False

    def update(self):
        newpos = self.calcnewpos(self.rect,self.vector)
        #collisioncheck with player
        #if newpos.collidedict(existinginstances) == "player":
        #    self.kill()
        self.rect = newpos
        #Make ball bounce from windowborders
        (angle,z) = self.vector
        if not self.area.contains(newpos):
            from math import pi
            tl = not self.area.collidepoint(newpos.topleft)
            tr = not self.area.collidepoint(newpos.topright)
            bl = not self.area.collidepoint(newpos.bottomleft)
            br = not self.area.collidepoint(newpos.bottomright)
            if tr and tl or (br and bl):
                angle = -angle
            if tl and bl:
                angle = pi - angle
            if tr and br:
                angle = pi - angle
        self.vector = (angle,z)
        

    def calcnewpos(self,rect,vector):
        (angle,z) = vector
        (dx, dy) = (z*math.cos(angle), z*math.sin(angle))
        self.movepos = [dx,dy]
        return rect.move(dx,dy)

    def Collide(self, collideobject):
        collideobject.movepos[1] = -collideobject.speed

    def __del__(self):
        badGuysSprites.add(bounceBall(self.mediator,(random.random()*2,5), [0,0]))
        badGuysSprites.add(bounceBall(self.mediator,(random.random()*2,5), [0,0]))

class bouncyBall(pygame.sprite.Sprite, phys.ProjectilePhysics):
    """A ball that bounces from objects
    """
    image = None
    
    def __init__(self, mediator, container, startLocation):
        pygame.sprite.Sprite.__init__(self)
        phys.ProjectilePhysics.__init__(self, container, 1, 5)
        self.mediator = mediator
        self.container = container

        if bounceBall.image is None:
            bounceBall.image, bounceBall.rect = imgLoad('ball1.png')
            
        self.image = bounceBall.image
        self.rect = self.image.get_rect()
        self.area = self.container.screen.get_rect()
        self.rect.topleft = startLocation
        self.deadly = False
        #self.movepos = [0,0]

    def update(self):
        #self.rect = self.rect.move(self.movepos)
        phys.ProjectilePhysics.update(self)
    
    def Collide(self, collideobject):
        print "ouch!"

class gravityBouncyBall(pygame.sprite.Sprite, phys.ProjectilePhysics):
    """A ball with gravity that bounces from objects
    """
    image = None
    
    def __init__(self, mediator, startLocation):
        pygame.sprite.Sprite.__init__(self)
        phys.ProjectilePhysics.__init__(self,1,5,True)
        self.mediator = mediator

        if bounceBall.image is None:
            bounceBall.image, bounceBall.rect = imgLoad('ball1.png')
            
        self.image = bounceBall.image
        self.rect = self.image.get_rect()
        self.area = screen.get_rect()
        self.rect.topleft = startLocation
        self.deadly = False
        #self.movepos = [0,0]

    def update(self):
        #self.rect = self.rect.move(self.movepos)
        phys.ProjectilePhysics.update(self)
    
    def Collide(self, collideobject):
        print "ouch!"

