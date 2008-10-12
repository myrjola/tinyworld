#
#
# menubutton.py
#
# Desc: Buttons used in the menusystem
#
#

import os, sys

import pygame
from pygame.locals import *

sys.path.insert(0, os.path.join("lib")) 

from gamefunc import *

class menuButton(pygame.sprite.Sprite):
    def __init__(self, text, callback, pos):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 18)
        self.buttonimg, self.rect = imgLoad('menubutton.png') 
        self.inactiveimg = self.buttonimg.copy()
        self.inactiveimg.blit(self.font.render(text, True, [0, 0, 0]), (10, 10))
        self.activeimg = self.buttonimg.copy()
        self.activeimg.blit(self.font.render(text, True, [255, 0, 0]), (10, 10))
        self.image = self.inactiveimg
        self.rect.topleft = pos
        self.callback = callback

    def activate(self):
        self.image = self.activeimg
    def deactivate(self):
        self.image = self.inactiveimg


