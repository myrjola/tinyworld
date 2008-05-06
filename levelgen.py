
import pygame, sys, os, pickle
from pygame.locals import *

#makes importing of modules in lib directory possible
sys.path.insert(0, os.path.join("lib")) 
from gamefunc import *

listorder = ["mainchar","badguys","balls","platforms","walls"]
spritelist = ["char2.png","badguy1.png","ball1.png","solid.png","wall.png"]
leveldatadict = {"mainchar":[],"badguys":[],"balls":[],"platforms":[],"walls":[]}
listorderindex = 0
charlist = []
badguylist = []
platflist = []
wallist = []
level = str(raw_input('which level name? --> '))


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
                if event.button == 1:
                    mousepos = pygame.mouse.get_pos()
                    leveldatadict[listorder[listorderindex]].append(mousepos)
                    img, rect = load_png(spritelist[listorderindex])
                    screen.blit(img,mousepos)
                if event.button == 3:
                    listorderindex += 1
                    try: print listorder[listorderindex]
                    except IndexError: listorderindex = 0

                print event.button
                print pygame.mouse.get_pos()
    pygame.display.flip()
print leveldatadict


#TODO make mouse driven level editor


'''
charlist.append([400,200])
badguylist.append([400,200])
platformlist = [[390,600],[390,300],[390,390]]
wallist = [[390,300],[700,300]]
'''


fullname = os.path.join('levels',level)
levelfile = open(fullname, 'w')
pickle.dump(leveldatadict, levelfile)
print "level generated"


