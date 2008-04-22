
import pygame, sys, os, pickle
from pygame.locals import *

charlist = []
badguylist = []
platflist = []
wallist = []
level = str(raw_input('which level name? '))


pygame.init()
screen = pygame.display.set_mode([1024,768])
background = pygame.Surface([1024,768])
background.fill([255,255,255])
screen.blit(background,[0,0])
pygame.display.flip()
running = 1

while running == 1:
    if pygame.mouse.get_focused:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = 0
            if event.type == MOUSEBUTTONDOWN:
                print event.button


#TODO make mouse driven level editor


charlist.append([400,200])
badguylist.append([400,200])
platformlist = [[390,600],[390,300],[390,390]]
wallist = [[390,300],[700,300]]





leveldatalist = [[charlist],[badguylist],[platformlist],[wallist]]
print leveldatalist

fullname = os.path.join('levels',level)
levelfile = open(fullname, 'w')
pickle.dump(leveldatalist, levelfile)


