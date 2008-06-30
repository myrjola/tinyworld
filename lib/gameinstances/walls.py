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
    

