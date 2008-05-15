#######################################
# gameinstances.py
# Author: Martin Yrjola
# library including all ingame instances in my platformer
#######################################

import math, os, sys, pygame, pickle, random
from pygame.locals import *

#makes importing of modules in lib directory possible
sys.path.insert(0, os.path.join("lib")) 

from gamefunc import *
from modelviewcontrol import *

global screen
screen = pygame.display.get_surface()


class PlatformerPhysics:
    '''Main object for objects that need physics
       like gravity, collision with walls etc.
    '''
    def __init__(self):
        print "Physics initiated"

    def update(self):
        if self.newpos.move(0,1).collidelist(walls) == -1: #not standing on ground
            if self.movepos[1] <= 12:
                self.movepos[1] += 1 #gravity

        self.newpos = self.WallCollisionCheck(self.newpos)

    def WallCollisionCheck(self, newpos):
        movepos = self.movepos
        colindex = newpos.collidelist(walls)
 
        #collision with horisontal platforms
        if colindex != -1:
            if movepos[1] <= 0: #going up
                if walls[colindex].bottom <= self.rect.top: #wall overtop
                    movepos[1] = walls[colindex].bottom - self.rect.top 
                    newpos = self.rect.move(movepos)
          
            elif movepos[1] >= 0: #going down
                if walls[colindex].top >= self.rect.bottom: #wall underneath
                    movepos[1] = walls[colindex].top - self.rect.bottom 
                    newpos = self.rect.move(movepos)
                    self.jumpable = self.jumpabletimes
    
        colindex = newpos.collidelist(walls)
        #collision with vertical walls
        if colindex != -1:
            if movepos[0] <= 0: #going left
                if walls[colindex].right <= self.rect.left: #wall on the left side
                    movepos[0] = walls[colindex].right - self.rect.left 
                    newpos = self.rect.move(movepos)
          
            elif movepos[0] >= 0: #going right
                if walls[colindex].left >= self.rect.right: #wall on the right side
                    movepos[0] = walls[colindex].left - self.rect.right 
                    newpos = self.rect.move(movepos)

 
        return newpos
   
class ProjectilePhysics:
    '''A superclass for all projectiles bouncing off walls'''

    def __init__(self, angle, speed, gravity=None):
        print "Projectile Physics initiated"
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
        colindex = newpos.collidelist(walls)
        pi = math.pi
 
        #collision with horisontal platforms
        if colindex != -1:
            if movepos[1] <= 0: #going up
                if walls[colindex].bottom <= self.rect.top: #wall overtop
                    movepos[1] = walls[colindex].bottom - self.rect.top 
                    newpos = self.rect.move(movepos)
                    self.angle = -self.angle
          
            elif movepos[1] >= 0: #going down
                if walls[colindex].top >= self.rect.bottom: #wall underneath
                    movepos[1] = walls[colindex].top - self.rect.bottom 
                    newpos = self.rect.move(movepos)
                    self.angle = -self.angle
    
        colindex = newpos.collidelist(walls)
        #collision with vertical walls
        if colindex != -1:
            if movepos[0] <= 0: #going left
                if walls[colindex].right <= self.rect.left: #wall on the left side
                    movepos[0] = walls[colindex].right - self.rect.left 
                    newpos = self.rect.move(movepos)
                    self.angle = pi - self.angle
          
            elif movepos[0] >= 0: #going right
                if walls[colindex].left >= self.rect.right: #wall on the right side
                    movepos[0] = walls[colindex].left - self.rect.right 
                    newpos = self.rect.move(movepos)
                    self.angle = pi - self.angle
        return newpos

        

    def calcnewpos(self):
        dx, dy = self.speed*math.cos(self.angle), self.speed*math.sin(self.angle)
        self.movepos = [dx, dy]
        newpos = self.rect.move(self.movepos)
        if newpos.move(0,1).collidelist(walls) == -1: #not standing on ground
            if self.gravity:
                if self.movepos[1] <= 31:
                    self.movepos[1] += 1 #gravity
                    self.angle = math.atan2(self.movepos[1],self.movepos[0])
        return self.movepos
        

class MainChar(pygame.sprite.Sprite, PlatformerPhysics):
    """The main character of the game
    """
    image = None

    def __init__(self, observer, startLocation):
        pygame.sprite.Sprite.__init__(self)
        PlatformerPhysics.__init__(self)
        self.observer = observer
        self.observer.addObserver(self)
        if MainChar.image == None:
            MainChar.image, MainChar.rect = load_png('char2.png')

        self.image = MainChar.image
        self.imageright = self.image
        self.imageleft = pygame.transform.flip(self.imageright, True, False)
        #screen = pygame.display.get_surface()
        self.rect = self.image.get_rect()
        self.startLocation = startLocation
        self.rect.topleft = startLocation
        self.area = screen.get_rect()
        self.speed = 9
        self.movepos = [0,0]
        self.jumpable = 1
        self.jumpabletimes = 2
        self.direction = None
        self.state = "still"
        MAINCHARALIVE = True

        goodGuysSprites.add(self)

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
            elif self.rect.left >= self.area.right:
                levelcord[0] = 1
            elif self.rect.top >= self.area.bottom:
                levelcord[1] = 1
            elif self.rect.bottom <= self.area.top:
                levelcord[1] = -1
            self.observer.inform(LevelChange(levelcord[0],levelcord[1]))
            

        self.rect = self.newpos #move the character
        
    def StopMoving(self):
        self.movepos[0] = 0 

    def MoveLeft(self, speed): 
        newpos = self.rect.move(-1,self.movepos[1])
        if newpos.collidelist(walls) == -1:
            self.movepos[0] = speed

    def MoveRight(self, speed):
        newpos = self.rect.move(1,self.movepos[1])
        if newpos.collidelist(walls) == -1:
            self.movepos[0] = speed

    def Jump(self):
        newpos = self.rect.move(self.movepos[0],-1)
        if newpos.collidelist(walls) == -1:
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
        pass

    

class bounceBall(pygame.sprite.Sprite):
    """A ball that bounces around the screen
    """
    image = None
    
    def __init__(self, observer, vector, startLocation):
        pygame.sprite.Sprite.__init__(self)
        self.observer = observer
        #self.observer.addObserver( self )

        if bounceBall.image is None:
            bounceBall.image, bounceBall.rect = load_png('ball1.png')
            
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
        badGuysSprites.add(bounceBall(self.observer,(random.random()*2,5), [0,0]))
        badGuysSprites.add(bounceBall(self.observer,(random.random()*2,5), [0,0]))
        
class badGuy(pygame.sprite.Sprite, PlatformerPhysics):
    image = None
    def __init__(self,observer,startLocation):
        pygame.sprite.Sprite.__init__(self)
        PlatformerPhysics.__init__(self)
        self.observer = observer
        if badGuy.image is None:
            badGuy.image, badGuy.rect = load_png('badguy1.png')

        self.image = badGuy.image
        self.imageright = self.image
        self.imageleft = pygame.transform.flip(self.imageright,True,False)
        self.rect = self.image.get_rect()
        self.area = screen.get_rect()
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
        if mainchar.rect.centerx >= self.rect.right: 
            self.MoveRight(self.speed)
            self.image = self.imageright
        elif mainchar.rect.centerx <= self.rect.left:
            self.MoveLeft(-self.speed)
            self.image = self.imageleft
        else:
            self.StopMoving()

    def StopMoving(self):
        self.movepos[0] = 0 

    def MoveLeft(self, speed): 
        newpos = self.rect.move(-1,self.movepos[1])
        if newpos.collidelist(walls) == -1:
            self.movepos[0] = speed

    def MoveRight(self, speed):
        newpos = self.rect.move(1,self.movepos[1])
        if newpos.collidelist(walls) == -1:
            self.movepos[0] = speed

    def Jump(self):
        if self.jumpable >= 1:
            self.jumpable -= 1
            self.movepos[1] = -2*self.speed
     

    def Collide(self, collideobject):
        print "bigouch!"

    def __del__(self):
        badGuysSprites.add(badGuy(self.observer, [0,0]))

class solidPlatform(pygame.sprite.Sprite):
    image = None
    def __init__(self, startLocation):
        pygame.sprite.Sprite.__init__(self)
        if solidPlatform.image is None:
            solidPlatform.image, solidPlatform.rect = load_png('solid.png')

        self.image = solidPlatform.image
        self.rect = self.image.get_rect()
        self.rect.topleft = startLocation
        walls.append(self.rect)
    

class solidWall(pygame.sprite.Sprite):
    image = None
    def __init__(self, startLocation):
        pygame.sprite.Sprite.__init__(self)
        if solidWall.image is None:
            solidWall.image, solidWall.rect = load_png('wall.png')
        
        self.image = solidWall.image
        self.rect = self.image.get_rect()
        self.area = screen.get_rect()
        self.rect.topleft = startLocation
        walls.append(self.rect)
    
class bouncyBall(pygame.sprite.Sprite, ProjectilePhysics):
    """A ball that bounces from objects
    """
    image = None
    
    def __init__(self, observer, startLocation):
        pygame.sprite.Sprite.__init__(self)
        ProjectilePhysics.__init__(self,1,5)
        self.observer = observer

        if bounceBall.image is None:
            bounceBall.image, bounceBall.rect = load_png('ball1.png')
            
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


class gravityBouncyBall(pygame.sprite.Sprite, ProjectilePhysics):
    """A ball with gravity that bounces from objects
    """
    image = None
    
    def __init__(self, observer, startLocation):
        pygame.sprite.Sprite.__init__(self)
        ProjectilePhysics.__init__(self,1,5,True)
        self.observer = observer

        if bounceBall.image is None:
            bounceBall.image, bounceBall.rect = load_png('ball1.png')
            
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


        

        

        

        

            
'''
            ############## The Levels ################
'''
class Level1:
    def __init__(self, observer):
        self.observer = observer
        player = MainChar(observer, [400,200])
        self.ball = bounceBall(observer, (1,5), [400,200])
        platform = solidPlatform([390,600])
        platform1 = solidPlatform([390,300])
        platform2 = solidPlatform([390,390])
        wall = solidWall([390,300])
        badGuysSprites.add(player, self.ball, platform, platform1, platform2, wall)



