
import pygame
import sys
import os
import pickle
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

pygame.init()
screen = pygame.display.set_mode([1024,768])
background = pygame.Surface([1024,768])
background.fill([255,255,255])
levelmapimg = load_png('levelmap.png')[0]
screen.blit(levelmapimg,[0,0])
pygame.display.flip()
running = 1
objsprites = pygame.sprite.Group()
mousesprite = pygame.sprite.RenderUpdates()
mousepos = (0,0)


class mouseSprite(pygame.sprite.Sprite):
    def __init__(self, (image,rect)):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = image,rect
    def update(self, image=None):
        self.rect.topleft = mousepos
        if image:
            self.image = image


class imgOfObject(pygame.sprite.Sprite):
    def __init__(self, (image,rect), pos):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = image,rect
        self.rect.topleft = pos

def alignToGrid((x,y)):
    #makes use of pythons way of rounding to integers
    xout = x/32*32
    yout = y/32*32
    return (xout,yout)

def chooseLevel():
    #Choose the level from the grid
    while 1:
        if pygame.mouse.get_focused:

            mousepos = alignToGrid(pygame.mouse.get_pos())
            for event in pygame.event.get():
                if event.type == QUIT:
                    raise SystemExitStatus('message')
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        global level
                        level = str(pygame.mouse.get_pos()[0]/64) + \
                                str(pygame.mouse.get_pos()[1]/64) 
                        print "You chose: ", level
                        return
    
# Make the screen ready for mapmaking
def makeLevel(): 
    running = 1
    screen.blit(background,[0,0])
    pygame.display.flip()
    listorder = ["mainchar","badguys","balls","platforms","walls"]
    spritelist = ["char2.png","badguy1.png","ball1.png","solid.png","wall.png"]
    leveldatadict = {"mainchar":[],"badguys":[],"balls":[],"platforms":[],"walls":[]}
    listorderindex = 0
    charlist = []
    badguylist = []
    platflist = []
    wallist = []
    imgrect = load_png(spritelist[listorderindex])
    mousesprite.add(mouseSprite(imgrect))
    global mousepos
    global leveldatadict

    # The levelmaking interface
    while 1:
        if pygame.mouse.get_focused:
            mousepos = alignToGrid(pygame.mouse.get_pos())
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mousepos = alignToGrid(pygame.mouse.get_pos())
                        leveldatadict[listorder[listorderindex]].append(mousepos)
                        background.blit(imgOfObject(imgrect,mousepos).image, mousepos)
    #                    objsprites.add(imgOfObject(imgrect,mousepos))
                    if event.button == 3:
                        listorderindex += 1
                        try: 
                            print listorder[listorderindex]
                            imgrect = load_png(spritelist[listorderindex])
                            mousesprite.update(imgrect[0])
                        except IndexError: 
                            listorderindex = 1
                            imgrect = load_png(spritelist[listorderindex])
                            mousesprite.update(imgrect[0])


                    print event.button
                    print pygame.mouse.get_pos()
        
        mousesprite.update()
        objsprites.draw(background)
        screen.blit(background,(0,0))
        pygame.display.update(mousesprite.draw(screen))
    print leveldatadict




'''
charlist.append([400,200])
badguylist.append([400,200])
platformlist = [[390,600],[390,300],[390,390]]
wallist = [[390,300],[700,300]]
'''
#Start levelmaking
chooseLevel()
makeLevel()


#Save image of level
imagepath = os.path.join('images','levelmap.png')
minimg = pygame.transform.scale(background,(64,64))
levelmapimg.blit(minimg,[int(level[0])*64,int(level[1])*64])
pygame.image.save(levelmapimg,imagepath)




#Save level
print leveldatadict
fullpath = os.path.join('levels',level)
levelfile = open(fullpath, 'w')
pickle.dump(leveldatadict, levelfile)
print "level generated"


