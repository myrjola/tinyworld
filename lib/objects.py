'''
library including all objects included in the game.
Somehow it was impossible to split MVC events and in-game
characters in different files.
'''

import math, os, sys, pygame
from pygame.locals import *

#makes importing of modules in lib directory possible
sys.path.insert(0, os.path.join("lib")) 
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
global CharMoveRequest
class CharMoveRequest(Event):
    def __init__(self, direction):
    	self.name = "Charactor Move Request"
    	self.direction = direction

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
    		#TODO: Handle input events
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
                        ev = CharMoveRequest('stopverticalmovement')
                        
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
    	self.screen = pygame.display.set_mode([1024,768])
    	self.spritegroup = pygame.sprite.RenderUpdates()
    	player = mainChar(evManager, [400,200])
    	self.ball = bounceBall(evManager, (1,5), [400,200])
        platform = solidPlatform([390,600])
        platform1 = solidPlatform([390,300])
        platform2 = solidPlatform([390,390])
        wall = solidWall([390,300])
    	self.spritegroup.add(player, self.ball, platform, platform1, platform2, wall)
    	self.background = pygame.Surface([1024, 768])
    	self.background.fill([255,255,255])
    	self.screen.blit(self.background, [0,0])
    	pygame.display.flip()
    		
    	
    def Notify(self, event):
    	if isinstance( event, TickEvent ):
    		#TODO; draw everything
    		self.spritegroup.update()
    		rectlist = self.spritegroup.draw(self.screen)
    		pygame.display.update(rectlist)
    		self.spritegroup.clear(self.screen, self.background)

    		
'''
##################### END OF MVC and mediator objects####################
'''


class mainChar(pygame.sprite.Sprite):
    """The main character of the game
    """
    image = None

    def __init__(self, evManager, startLocation):
    	pygame.sprite.Sprite.__init__(self)
    	self.evManager = evManager
    	self.evManager.RegisterListener(self)
    	if mainChar.image == None:
    		mainChar.image, mainChar.rect = load_png('char2.png')

    	self.image = mainChar.image
    	screen = pygame.display.get_surface()
    	self.rect = self.image.get_rect()
    	self.rect.topleft = startLocation
        self.area = screen.get_rect()
        self.speed = 9
        self.movepos = [0,0]
        self.jumpable = 1
        self.jumpabletimes = 2
        self.direction = "none"

    def update(self):

        newpos = self.rect.move(self.movepos)
        if self.movepos[1] <= 12:
            self.movepos[1] += 1 #gravity

        if newpos.collidelist(walls) != -1:
            newpos = self.rect.move([0,self.movepos[1]])

        if self.movepos[1] >= 0 and newpos.collidelist(platformlist) != -1: #nocollide = -1
            while newpos.collidelist(platformlist) != -1: #make soft landing
                self.movepos[1] -=1
                newpos = self.rect.move([0,self.movepos[1]])
            newpos = self.rect.move([self.movepos[0],0])
            self.jumpable = self.jumpabletimes
        if self.movepos[1] <= 0 and newpos.collidelist(platformlist) != -1: #nocollide = -1
            while newpos.collidelist(platformlist) != -1: #make soft headbump
                self.movepos[1] +=1
                newpos = self.rect.move([-self.movepos[0],self.movepos[1]])
            newpos = self.rect.move([self.movepos[0],0])
        
 
            
        self.rect = newpos #move the character



    def Notify(self, event):
        if isinstance(event, CharMoveRequest):
            self.move = event.direction
            if self.move == "left":
                self.direction = "left"
                self.movepos[0] = -self.speed
            elif self.move == "right":
                self.direction = "right"
                self.movepos[0] = self.speed
            elif self.move == "jump":
                if self.jumpable >= 1:
                    self.jumpable -= 1
                    self.movepos[1] = -2*self.speed
                    
            elif self.move == "stopverticalmovement":
                self.direction = "none"
                self.movepos[0] = 0
    
    def __del__(self):
        evManager.Notify(CharacterDeadEvent())




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
    	screen = pygame.display.get_surface()
    	self.area = screen.get_rect()
    	self.vector = vector
    	self.rect.topleft = startLocation
    def update(self):
    	newpos = self.calcnewpos(self.rect,self.vector)
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

    	
class badGuy(pygame.sprite.Sprite):
    image = None
    def __init__(self,evManager,startLocation):
        pygame.sprite.Sprite.__init__(self)
        self.evManager = evManager
        if badGuy.image is None:
            badGuy.image, badGuy.rect = load_png('badguy1.png')

        self.image = badGuy.image
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = startLocation
    
    def update(self):
        newpos = self.rect.move(1,1)
        self.rect = newpos

class solidPlatform(pygame.sprite.Sprite):
    image = None
    def __init__(self, startLocation):
        pygame.sprite.Sprite.__init__(self)
        if solidPlatform.image is None:
            solidPlatform.image, solidPlatform.rect = load_png('solid.png')

        self.image = solidPlatform.image
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.rect.topleft = startLocation
        wall1 = platformWall(startLocation)
        wall2 = platformWall(self.rect.topright)
        platformlist.append(self.rect)
    

class solidWall(pygame.sprite.Sprite):
    image = None
    def __init__(self, startLocation):
        pygame.sprite.Sprite.__init__(self)
        if solidWall.image is None:
            solidWall.image, solidWall.rect = load_png('wall.png')
        
        self.image = solidWall.image
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = startLocation
        walls.append(self.rect)
        platformlist.append(Rect((self.rect.bottomleft,[self.rect.width, 1])).inflate(-5,0))
        platformlist.append(Rect((self.rect.topleft,[self.rect.width, 1])).inflate(-5,0))
        

        
class platformWall:
    def __init__(self,startLocation):
        self.rect = Rect(startLocation,[1,17])
        walls.append(self.rect)
        screen = pygame.display.get_surface()

            
