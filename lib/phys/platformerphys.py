
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



########### Base Classes ##############################

class PlatformerPhysics:
    '''Main object for objects that need physics
       like gravity, collision with walls etc.
    '''
    def __init__(self, container):
        self.container = container
        self.solidwalls = self.container.solidwalls
        print "Physics initiated"

    def update(self):
        if self.newpos.move(0,1).collidelist(self.container.solidwalls) == -1: 
            #not standing on ground
            if self.movepos[1] <= 12:
                self.movepos[1] += 1 #gravity

        self.newpos = self.WallCollisionCheck(self.newpos)

    def WallCollisionCheck(self, newpos):
        movepos = self.movepos
        colindex = newpos.collidelist(self.container.solidwalls)
 
        #collision with horisontal platforms
        if colindex != -1:
            if movepos[1] <= 0: #going up
                if self.container.solidwalls[colindex].bottom <= self.rect.top:
                    #wall overtop
                    movepos[1] = self.container.solidwalls[colindex].bottom -\
                            self.rect.top 
                    newpos = self.rect.move(movepos)
          
            elif movepos[1] >= 0: #going down
                if self.container.solidwalls[colindex].top >= self.rect.bottom: 
                    #wall underneath
                    movepos[1] = self.container.solidwalls[colindex].top -\
                            self.rect.bottom 
                    newpos = self.rect.move(movepos)
                    self.jumpable = self.jumpabletimes
    
        colindex = newpos.collidelist(self.container.solidwalls)
        #collision with vertical self.container.solidwalls
        if colindex != -1:
            if movepos[0] <= 0: #going left
                if self.container.solidwalls[colindex].right <= self.rect.left: 
                    #wall on the left side
                    movepos[0] = self.container.solidwalls[colindex].right -\
                            self.rect.left 
                    newpos = self.rect.move(movepos)
          
            elif movepos[0] >= 0: #going right
                if self.container.solidwalls[colindex].left >= self.rect.right: 
                    #wall on the right side
                    movepos[0] = self.container.solidwalls[colindex].left -\
                            self.rect.right 
                    newpos = self.rect.move(movepos)

 
        return newpos
   
