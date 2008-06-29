#######################################
# gameinstances.py
# Author: Martin Yrjola
# library including all ingame instances in my platformer
#######################################
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
        
########### Sub Classes ###############################

class MainChar(pygame.sprite.Sprite, PlatformerPhysics):
    """The main character of the game
    """
    image = None

    def __init__(self, mediator, container, startLocation):
        pygame.sprite.Sprite.__init__(self)
        PlatformerPhysics.__init__(self, container)
        self.mediator = mediator
        self.mediator.addObserver(self)
        self.container = container
        if MainChar.image == None:
            MainChar.image, MainChar.rect = imgLoad('char2.png')

        self.image = MainChar.image
        self.imageright = self.image
        self.imageleft = pygame.transform.flip(self.imageright, True, False)
        #screen = screen
        self.rect = self.image.get_rect()
        self.startLocation = startLocation
        self.rect.topleft = startLocation
        self.area = self.container.screen.get_rect()
        self.speed = 9.0
        self.movepos = [0,0]
        self.jumpable = 1
        self.jumpabletimes = 2
        self.direction = None
        self.state = "still"
        MAINCHARALIVE = True

        #goodGuysSprites.add(self)

    def update(self):

        self.newpos = self.rect.move(self.movepos)
        if self.direction == "left":
            self.MoveLeft(-self.speed)
            self.image = self.imageleft
        elif self.direction == "right":
            self.MoveRight(self.speed)
            self.image = self.imageright
        else: self.StopMoving()

        PlatformerPhysics.update(self)
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
            self.rect = self.newpos # to avoid levelchange loop
            self.mediator.inform(LevelChange(levelcord[0],levelcord[1]))
            

        self.rect = self.newpos #move the character

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
        else:
            collideobject.kill()

    
    def inform(self, event):
        if event.name == 'MoveChar':
            self.move = event.direction
            self.state = "moving"
            if self.move == "left":
                self.direction = "left"
                self.movepos[0] = -self.speed
                
            elif self.move == "right":
                self.direction = "right"
                self.movepos[0] = self.speed
 
            elif self.move == "jump":
                self.Jump()
                   
            elif self.move == "stophorisontalmovement":
                self.direction = None
                self.state = "still"
                self.movepos[0] = 0
    
    def __del__(self):
        self.mediator.delObserver(self)

    

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
        
class badGuy(pygame.sprite.Sprite, PlatformerPhysics):
    image = None
    def __init__(self,mediator, container, startLocation):
        pygame.sprite.Sprite.__init__(self)
        PlatformerPhysics.__init__(self, container)
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
        PlatformerPhysics.update(self)
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
        badGuysSprites.add(badGuy(self.mediator, [0,0]))

class solidPlatform(pygame.sprite.Sprite):
    image = None
    def __init__(self, startLocation):
        pygame.sprite.Sprite.__init__(self)
        if solidPlatform.image is None:
            solidPlatform.image, solidPlatform.rect = imgLoad('solid.png')

        self.image = solidPlatform.image
        self.rect = self.image.get_rect()
        self.rect.topleft = startLocation
    

class solidWall(pygame.sprite.Sprite):
    image = None
    def __init__(self, startLocation):
        pygame.sprite.Sprite.__init__(self)
        if solidWall.image is None:
            solidWall.image, solidWall.rect = imgLoad('wall.png')
        
        self.image = solidWall.image
        self.rect = self.image.get_rect()
        self.rect.topleft = startLocation
    
class bouncyBall(pygame.sprite.Sprite, ProjectilePhysics):
    """A ball that bounces from objects
    """
    image = None
    
    def __init__(self, mediator, container, startLocation):
        pygame.sprite.Sprite.__init__(self)
        ProjectilePhysics.__init__(self, container, 1, 5)
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
        ProjectilePhysics.update(self)
    
    def Collide(self, collideobject):
        print "ouch!"

class gravityBouncyBall(pygame.sprite.Sprite, ProjectilePhysics):
    """A ball with gravity that bounces from objects
    """
    image = None
    
    def __init__(self, mediator, startLocation):
        pygame.sprite.Sprite.__init__(self)
        ProjectilePhysics.__init__(self,1,5,True)
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
        ProjectilePhysics.update(self)
    
    def Collide(self, collideobject):
        print "ouch!"

