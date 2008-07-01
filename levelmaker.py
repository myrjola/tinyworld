# 
# File: levelmaker.py
# Author: Martin Yrjola
# Desc: A levelmaker for the platformer
#       Will be of great help when making
#       the game.
#
import pygame
import sys
import os
import pickle
from pygame.locals import *

# using gooeypy as gui
from gooeypy import sdl as gui
from gooeypy.const import *

#makes importing of modules in lib directory possible
sys.path.insert(0, os.path.join("lib")) 
from gamefunc import *

class LevelMaker:
    '''
    contains data and functions needed to make levels
    '''
    def __init__(self):
        self.listorder = ["mainchar","badguys","balls","platforms","walls"]
        self.spritelist = ["char2.png","badguy1.png","ball1.png","solid.png","wall.png"]
        self.leveldatadict = {"mainchar":[],"badguys":[],"balls":[],"platforms":[],"walls":[]}
        self.listorderindex = 0
        self.charlist = []
        self.badguylist = []
        self.platflist = []
        self.wallist = []
        self.levelmapimg = imgLoad('levelmap.png')[0] # we only need the image
        self.background = pygame.display.get_surface()
        self.level = '00'

    def saveLevel(self):
        #Save image of level
        imagepath = os.path.join('images','levelmap.png')
        minimg = pygame.transform.scale(self.background,(64,64))
        self.levelmapimg.blit(minimg,[int(self.level[0])*64,int(self.level[1])*64])
        pygame.image.save(self.levelmapimg, imagepath)

        #Save level
        print self.leveldatadict
        fullpath = os.path.join('levels', self.level)
        levelfile = open(fullpath, 'w')
        pickle.dump(self.leveldatadict, levelfile)
        print "level saved"

class GuiContainer(gui.Container):
    '''
    takes care of the widgets
    '''
    def activate(self, index):
        for w in self.widgets:
            w.active = False
        self.widgets[index].active = True

class mouseSprite(pygame.sprite.Sprite):
    '''
    paints the mouse cursor as the object to add to the level
    '''
    def __init__(self, (image,rect)):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = image,rect
    def update(self, image=None):
        self.rect.topleft = mousepos
        if image:
            self.image = image


class addedObject(pygame.sprite.Sprite):
    def __init__(self, (image,rect), pos):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = image,rect
        self.rect.topleft = pos

def alignToGrid((x,y)):
    '''
    aligns the objects to 32*32 grids
    '''
    xout = x/32*32
    yout = y/32*32
    return (xout,yout)


def main():
    # init pygame
    pygame.init()
    screen = pygame.display.set_mode([1280,1024])
    clock = pygame.time.Clock()
    levmak = LevelMaker()
    # init gooeypy
    gui.init(myscreen=screen)
    app = gui.App(width=1280, height=768)

    menus = GuiContainer(width=1280, height=768)
    app.add(menus)

    # the choose level state
    levelchange = gui.Container(width=1280, height=768)
    left_hbar1 = gui.HBox(align="left", valign="top", spacing=5)
    levelmap = gui.Image(levmak.levelmapimg)
    levelchange.add(levelmap)

    # the level making state
    levelmake = gui.Container(width=1280, height=768)
    save_button = gui.Button('save')
    save_button.connect(CLICK, levmak.saveLevel()) 
    back_button = gui.Button('change level')
    back_button.connect(CLICK, menus.activate, 0)
    
    left_hbar2 = gui.HBox(align="left", valign="top", spacing=5)
    levelmake.add(save_button, back_button)
    
    # now add them to the main container
    menus.add(levelchange, levelmake)

    # activate the choose level state
    menus.activate(0)

    running = True
    while running:
        clock.tick(35)
        events = pygame.event.get()

        for event in events:
            if event.type == QUIT:
                quit = True

        app.run(events)
        app.draw()

        gui.update_display()
    


    




if __name__ == '__main__':
    main()









pygame.init()
screen = pygame.display.set_mode([1280,768])
background = pygame.Surface([1280,768])
background.fill([255,255,255])
levelmapimg = imgLoad('levelmap.png')[0]
screen.blit(levelmapimg,[0,0])
pygame.display.flip()
running = 1
objsprites = pygame.sprite.Group()
mousesprite = pygame.sprite.RenderUpdates()
mousepos = (0,0)


def chooseLevel():
    #Choose the level from the grid
    while 1:
        if pygame.mouse.get_focused:

            mousepos = alignToGrid(pygame.mouse.get_pos())
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
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
    global leveldatadict
    leveldatadict = {"mainchar":[],"badguys":[],"balls":[],"platforms":[],"walls":[]}
    listorderindex = 0
    charlist = []
    badguylist = []
    platflist = []
    wallist = []
    imgrect = imgLoad(spritelist[listorderindex])
    mousesprite.add(mouseSprite(imgrect))
    global mousepos

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
                            imgrect = imgLoad(spritelist[listorderindex])
                            mousesprite.update(imgrect[0])
                        except IndexError: 
                            listorderindex = 1
                            imgrect = imgLoad(spritelist[listorderindex])
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
pygame.image.save(levelmapimg, imagepath)

#Save level
print leveldatadict
fullpath = os.path.join('levels',level)
levelfile = open(fullpath, 'w')
pickle.dump(leveldatadict, levelfile)
print "level generated"


