'''
library including all objects included in the game.
Somehow it was impossible to split MVC events and in-game
characters in different files.
'''

import math, os, sys, pygame, pickle, random
from pygame.locals import *

#makes importing of modules in lib directory possible
sys.path.insert(0, os.path.join("lib")) 
#import levels
from gamefunc import *
from main import *

global walls
walls = []
global mainCharAlive
mainCharAlive = False

class Event:
    """event superclass"""
    def __init__(self):
        self.name = "Generic Event"

class TickEvent(Event):
    def __init__(self):
        self.name = "CPU Tick Event"

class QuitEvent(Event):
    def __init__(self):
        self.name = "Program Quit Event"
class GameStartedEvent(Event):
    def __init__(self, game):
        self.name = "Game Started Event"
        self.game = game
class CharMoveRequest(Event):
    def __init__(self, direction):
        self.name = "Charactor Move Request"
        self.direction = direction
class DisplayReady(Event):
    def __init__(self):
        self.name = "Display Ready Event"
class LevelChange(Event):
    def __init__(self, x, y):
        self.name = "Level Change Event"
        self.left_or_right = x
        self.up_or_down = y

class EventManager:
    """The mediator betveen MVC"""
    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()
        self.eventQueue = []

    def RegisterListener(self, listener):
        self.listeners[ listener ] = 1
    
    def UnregisterListener(self, listener):
        if listener in self.listeners.keys():
            del self.listeners[ listener ]
    
    def Post(self, event):
        for listener in self.listeners.keys():
            #NOTE: If the weakref has died it will
            #be automatically removed, so we don't
            #have to worry about it
            listener.Notify(event)
    
    def Notify(self, event):
        for listener in self.listeners.keys():
            #If weakref has died, remove it and continue
            #through the list
            if listener is None:
                del self.listeners[listener]
                continue
            listener.Notify(event)


class KeyboardController:
    def __init__(self,evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
    def Notify(self, event):
        if isinstance(event, TickEvent):

            for event in pygame.event.get():
                ev = None
                if event.type == QUIT:
                    ev = QuitEvent()
                    
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        ev = QuitEvent()
                    elif event.key == K_UP:
                        ev = CharMoveRequest('jump')
                    elif event.key == K_DOWN:
                        ev = CharMoveRequest('duck')
                    elif event.key == K_LEFT:
                        ev = CharMoveRequest('left')
                    elif event.key == K_RIGHT:
                        ev = CharMoveRequest('right')
                    pygame.event.pump()
                    

                   
                elif event.type == KEYUP:
                    keys = pygame.key.get_pressed()
                    if not 1 in [keys[K_LEFT], keys[K_RIGHT]]:
                        ev = CharMoveRequest('stophorisontalmovement')
                        
                if ev:
                    self.evManager.Notify(ev)
    
    


class CPUSpinnerController:
    def __init__(self,evManager):
        #implement fps-limit
        self.clock = pygame.time.Clock()
        self.evManager = evManager
        self.keepGoing = 1

    def Run(self):
        while self.keepGoing:
            self.clock.tick(30)
            event = TickEvent()
            self.evManager.Notify(event)

    def Notify(self,event):
        if isinstance(event,QuitEvent):
            #stop the while loop
            self.keepGoing = 0

class PygameView:
    def __init__(self,evManager):
        self.evManager = evManager
        evManager.RegisterListener(self)
        global screen
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
        evManager.Notify(DisplayReady())
            
        
    def Notify(self, event):
        if isinstance( event, TickEvent ):
            badGuysSprites.update()
            goodGuysSprites.update()
            rectlist = badGuysSprites.draw(screen) + goodGuysSprites.draw(screen)
            pygame.display.update(rectlist)
            badGuysSprites.clear(screen, background)
            goodGuysSprites.clear(screen, background)

class LevelController:
    def __init__(self,evManager):
        self.evManager = evManager
        self.curlevel = [0,0]
        
    def Notify(self, event):
        if isinstance(event, DisplayReady):
            evManager = self.evManager
            self.CreateLevel(self.OpenLevelFile('00'))
        if isinstance(event, LevelChange):
            self.curlevel[0] += event.left_or_right
            self.curlevel[1] += event.up_or_down
            self.CreateLevel(self.OpenLevelFile(str(self.curlevel[0]) + str(self.curlevel[1])))



    def CreateLevel(self,level):
        evManager = self.evManager
        background.fill([255,255,255])
        badGuysSprites.empty()
        if mainCharAlive:
            mainchar.rect.topleft = [33,33]            
            goodGuysSprites.add(mainchar)

        walls = []
        for i in level["mainchar"]:
            global mainchar
            mainchar = mainChar(self.evManager,i)
        for i in level["badguys"]:
            badGuysSprites.add(badGuy(evManager, i))
        for i in level["balls"]:
            badGuysSprites.add(bouncyBall(evManager, i))
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
    A class that handles collisionmanagement
    '''

    def __init__(self, evManager):
        self.evManager = evManager

    def Notify(self, event):
        if isinstance( event, TickEvent ):
            collisions = pygame.sprite.groupcollide(goodGuysSprites, 
                    badGuysSprites, False, False) #returns dictionary
            for smashed in collisions: #"smashed"key returns collisionlist
                for colobj in collisions[smashed]:
                    print smashed, "collided with", colobj
                    colobj.Collide(smashed) #badguy collision event 
                    smashed.Collide(colobj) #goodguy collision event
        
        
        



        
        
        
        
        
        
            
'''
##################### END OF MVC and mediator objects####################
'''


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
        

class mainChar(pygame.sprite.Sprite, PlatformerPhysics):
    """The main character of the game
    """
    image = None

    def __init__(self, evManager, startLocation):
        pygame.sprite.Sprite.__init__(self)
        PlatformerPhysics.__init__(self)
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        if mainChar.image == None:
            mainChar.image, mainChar.rect = load_png('char2.png')

        self.image = mainChar.image
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
        mainCharAlive = True

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
            self.evManager.Notify(LevelChange(levelcord[0],levelcord[1]))
            

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

    
    def Notify(self, event):
        if isinstance(event, CharMoveRequest):
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
    
    def __init__(self, evManager, vector, startLocation):
        pygame.sprite.Sprite.__init__(self)
        self.evManager = evManager
        #self.evManager.RegisterListener( self )

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
        badGuysSprites.add(bounceBall(self.evManager,(random.random()*2,5), [0,0]))
        badGuysSprites.add(bounceBall(self.evManager,(random.random()*2,5), [0,0]))
        
class badGuy(pygame.sprite.Sprite, PlatformerPhysics):
    image = None
    def __init__(self,evManager,startLocation):
        pygame.sprite.Sprite.__init__(self)
        PlatformerPhysics.__init__(self)
        self.evManager = evManager
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
        badGuysSprites.add(badGuy(self.evManager, [0,0]))

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
    
    def __init__(self, evManager, startLocation):
        pygame.sprite.Sprite.__init__(self)
        ProjectilePhysics.__init__(self,1,5)
        self.evManager = evManager

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
        print "ouch! ball hit"


class gravityBouncyBall(pygame.sprite.Sprite, ProjectilePhysics):
    """A ball with gravity that bounces from objects
    """
    image = None
    
    def __init__(self, evManager, startLocation):
        pygame.sprite.Sprite.__init__(self)
        ProjectilePhysics.__init__(self,1,5,True)
        self.evManager = evManager

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
    def __init__(self, evManager):
        self.evManager = evManager
        player = mainChar(evManager, [400,200])
        self.ball = bounceBall(evManager, (1,5), [400,200])
        platform = solidPlatform([390,600])
        platform1 = solidPlatform([390,300])
        platform2 = solidPlatform([390,390])
        wall = solidWall([390,300])
        badGuysSprites.add(player, self.ball, platform, platform1, platform2, wall)



