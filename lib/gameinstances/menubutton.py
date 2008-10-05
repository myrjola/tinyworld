#
#
# menubutton.py
# 
# Desc: Buttons used in the menusystem
#
#

import pygame
from pygame.locals import *


class menuButton(pygame.sprite.Sprite):
    def __init__(self, text, callback, pos):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 18)
        self.inactiveimg = self.font.render(text, True, [0, 0, 0])
        self.activeimg = self.font.render(text, True, [255, 0, 0])
        self.image = self.inactiveimg
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.callback = callback

    def activate(self):
        self.image = self.activeimg
    def deactivate(self):
        self.image = self.inactiveimg


