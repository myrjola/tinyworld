import math
import os
import sys
import pickle
import random

import pygame
from pygame.locals import *

# makes importing of modules in lib directory possible
sys.path.insert(0, os.path.join("lib")) 

from events import *
from gamefunc import *

class ProjectilePhysics:
    '''A superclass for all projectiles bouncing off walls'''

    def __init__(self, container, angle, speed, gravity=None):
        print "Projectile Physics initiated"
        self.container = container
        self.angle = angle
        self.speed = speed
        self.gravity = gravity
        self.movepos = [0,0]

    def update(self):
        self.newpos = self.rect.move(self.calcnewpos())
        self.newpos = self.WallCollisionCheck(self.newpos)
        self.rect = self.newpos  

    def WallCollisionCheck(self, newpos):
        movepos = self.movepos
        colindex = newpos.collidelist(self.container.solidwalls)
        pi = math.pi
 
        #collision with horisontal platforms
        if colindex != -1:
            if movepos[1] <= 0: #going up
                if self.container.solidwalls[colindex].bottom <= self.rect.top: \
                        #wall overtop
                    movepos[1] = self.container.solidwalls[colindex].bottom - \
                            self.rect.top 
                    newpos = self.rect.move(movepos)
                    self.angle = -self.angle
          
            elif movepos[1] >= 0: #going down
                if self.container.solidwalls[colindex].top >= self.rect.bottom: \
                        #wall underneath
                    movepos[1] = self.container.solidwalls[colindex].top -\
                            self.rect.bottom 
                    newpos = self.rect.move(movepos)
                    self.angle = -self.angle
    
        colindex = newpos.collidelist(self.container.solidwalls)
        #collision with vertical walls
        if colindex != -1:
            if movepos[0] <= 0: #going left
                if self.container.solidwalls[colindex].right <= self.rect.left:\
                        #wall on the left side
                    movepos[0] = self.container.solidwalls[colindex].right -\
                            self.rect.left 
                    newpos = self.rect.move(movepos)
                    self.angle = pi - self.angle
          
            elif movepos[0] >= 0: #going right
                if self.container.solidwalls[colindex].left >= self.rect.right:\
                        #wall on the right side
                    movepos[0] = self.container.solidwalls[colindex].left -\
                            self.rect.right 
                    newpos = self.rect.move(movepos)
                    self.angle = pi - self.angle
        return newpos

        

    def calcnewpos(self):
        dx, dy = self.speed*math.cos(self.angle), self.speed*math.sin(self.angle)
        self.movepos = [dx, dy]
        newpos = self.rect.move(self.movepos)
        if newpos.move(0,1).collidelist(self.container.solidwalls) == -1: #not standing on ground
            if self.gravity:
                if self.movepos[1] <= 31:
                    self.movepos[1] += 1 #gravity
                    self.angle = math.atan2(self.movepos[1],self.movepos[0])
        return self.movepos
 
