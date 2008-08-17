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

class solidPlatform(pygame.sprite.Sprite):
    image = None
    def __init__(self, container, startLocation):
        pygame.sprite.Sprite.__init__(self)
        self.container = container
        if solidPlatform.image is None:
            solidPlatform.image, solidPlatform.rect = imgLoad('solid.png')

        self.image = solidPlatform.image
        self.rect = self.image.get_rect()
        self.rect.topleft = startLocation
        self.container.solidwalls.append(self.rect)
        self.container.background.blit(self.image, self.rect)
        del(self)
    
class solidWall(pygame.sprite.Sprite):
    image = None
    def __init__(self, container, startLocation):
        pygame.sprite.Sprite.__init__(self)
        self.container = container
        if solidWall.image is None:
            solidWall.image, solidWall.rect = imgLoad('wall.png')
        
        self.image = solidWall.image
        self.rect = self.image.get_rect()
        self.rect.topleft = startLocation
        self.container.solidwalls.append(self.rect)
        self.container.background.blit(self.image, self.rect)
        del(self)
    

