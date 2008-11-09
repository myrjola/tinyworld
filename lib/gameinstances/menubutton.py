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

class menuButton(pygame.sprite.DirtySprite):
    font = None
    def __init__(self, text, callback, pos):
        pygame.sprite.DirtySprite.__init__(self)
        if menuButton.font == None:
            menuButton.font = pygame.font.Font(None, 18)
        self.buttonimg, self.rect = imgLoad('menubutton.png') 
        self.inactiveimg = self.buttonimg.copy()
        self.inactiveimg.blit(menuButton.font.render(text, True, [0, 0, 0]), (10, 10))
        self.activeimg = self.buttonimg.copy()
        self.activeimg.blit(menuButton.font.render(text, True, [255, 0, 0]), (10, 10))
        self.image = self.inactiveimg
        self.rect.topleft = pos
        self.callback = callback

    def activate(self):
        self.image = self.activeimg
        self.dirty = 1
    def deactivate(self):
        self.image = self.inactiveimg
        self.dirty = 1

