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

global platformlist
platformlist = []
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
        
        
    def Notify(self, event):
        if isinstance(event, DisplayReady):
            evManager = self.evManager
            self.CreateLevel(self.OpenLevelFile('level3'))

    def CreateLevel(self,level):
        evManager = self.evManager
        for i in level["mainchar"]:
            global mainchar
            mainchar = mainChar(evManager, i)
        for i in level["badguys"]:
            badGuysSprites.add(badGuy(evManager, i))
        for i in level["balls"]:
            badGuysSprites.add(bounceBall(evManager, (1,5), i))
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
        if self.movepos[1] <= 12:
            self.movepos[1] += 1 #gravity

        #newpos = self.rect.move([0,self.movepos[1]])
        self.newpos = self.PlatformCollisionCheck(self.newpos)
        self.newpos = self.WallCollisionCheck(self.newpos)

    def WallCollisionCheck(self, newpos):
        movepos = self.movepos
        #collision with vertical walls
        if newpos.collidelist(walls) != -1:
            #newpos = self.rect.move([0,self.movepos[1]])
            
            #if self.direction == "left":
            if movepos[0] <= 0: #going left
                while newpos.collidelist(walls) != -1:
                    movepos[0] +=1
                    newpos = self.rect.move([movepos[0],0])
          
            elif movepos[0] >= 0: #going right
                while newpos.collidelist(walls) != -1:
                    movepos[0] -=1
                    newpos = self.rect.move([movepos[0],0])

        return newpos
   

    def PlatformCollisionCheck(self, newpos):
        #collision with horisontal platforms
        colindex = newpos.collidelist(platformlist) #returns index -> rect
        if self.movepos[1] >= 0 and colindex != -1:
            if platformlist[colindex].top << self.rect.bottom:
                while newpos.collidelist(platformlist) != -1: #make soft landing
                    self.movepos[1] -=1
                    newpos = self.rect.move([0,self.movepos[1]])
                newpos = self.rect.move([self.movepos[0],0])
                self.jumpable = self.jumpabletimes
        if self.movepos[1] <= 0 and colindex != -1: #nocollide = -1
            if platformlist[colindex].bottom << self.rect.top:
                while newpos.collidelist(platformlist) != -1: #make soft headbump
                    self.movepos[1] +=1
                    newpos = self.rect.move([-self.movepos[0],self.movepos[1]])
            newpos = self.rect.move([self.movepos[0],0])
        return newpos

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

        goodGuysSprites.add(self)

    def update(self):

        self.newpos = self.rect.move(self.movepos)
        if self.direction == "left":
            self.MoveLeft(-self.speed)
        elif self.direction == "right":
            self.MoveRight(self.speed)
        else: self.StopMoving()

        PlatformerPhysics.update(self)

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
        self.evManager.Notify(CharacterDeadEvent())

    

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
        self.rect = self.image.get_rect()
        self.area = screen.get_rect()
        self.rect.topleft = startLocation
        self.movepos = [0,0]
        self.jumpable = 1
        self.jumpabletimes = 5 
        self.speed = 5
        self.deadly = True
    
    def update(self):
        self.newpos = self.rect.move(self.movepos)
        PlatformerPhysics.update(self)
        self.rect = self.newpos
        if self.movepos[1] << 0: #Falling
            self.Jump()
        if not self.rect.colliderect(self.area):
            self.kill()

        if mainchar.rect.centerx >= self.rect.centerx: #chase mainchar
            self.MoveRight(self.speed)
        else:
            self.MoveLeft(-self.speed)

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
        wall1 = platformWall(startLocation)
        wall2 = platformWall((self.rect.topright[0] -1,self.rect.topright[1]))
        platformlist.append(self.rect)
    

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
        platformlist.append(Rect((self.rect.bottomleft,[self.rect.width, 1])))
        platformlist.append(Rect((self.rect.topleft,[self.rect.width, 1])))
    
        

        
class platformWall:
    def __init__(self,startLocation):
        self.rect = Rect(startLocation,[1,30])
        walls.append(self.rect)

            
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



