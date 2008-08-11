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

class LevelChoser:
    '''
    takes care of the level choosing state
    '''
    def __init__(self, app, menus):
        self.app = app
        self.menus = menus
        self.levelmapimg = imgLoad('levelmap.png')[0] # imgLoad returns surface, rect

    def chooseLevel(self):
    #Choose the level from the grid
        self.menus.activate(0)
        self.app.draw()
        gui.update_display()

        chosen = False
        while not chosen:

            if pygame.mouse.get_focused:

                # mousepos = self.alignToGrid(pygame.mouse.get_pos())
                for event in pygame.event.get():
                    if event.type == QUIT:
                        sys.exit()
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.level = str((pygame.mouse.get_pos()[0] - 256)/64) + \
                                    str(pygame.mouse.get_pos()[1]/64) 
                            print "You chose: ", self.level
                            chosen = True
                            
        self.menus.activate(1) 


class LevelMaker:
    '''
    takes care of the level making state
    '''
    def __init__(self, app, menus):
        self.app = app
        self.menus = menus

    def saveLevel(self):
        pass
        
    def alignToGrid(self, (x,y)):
        #makes use of pythons way of rounding to integers
        xout = x/32*32
        yout = y/32*32
        return (xout,yout)



class GuiContainer(gui.Container):
    '''
    takes care of switching between states
    '''
    def activate(self, index):
        for w in self.widgets:
            w.active = False
        self.widgets[index].active = True

def main():
    # init pygame
    pygame.init()
    screen = pygame.display.set_mode([1280,768])
    clock = pygame.time.Clock()
    # init gooeypy
    gui.init(myscreen=screen)
    app = gui.App(width=1280, height=768)

    menus = GuiContainer(width=1280, height=768)
    app.add(menus)

    # init the state classes
    levelchoser = LevelChoser(app, menus)
    levelmaker = LevelMaker(app, menus)

    # the choose level state
    levelchange = gui.Container(width=1280, height=768)
    empty_selbox = gui.SelectBox(width=256)
    levelmap = gui.Image(levelchoser.levelmapimg)
    hbar1 = gui.HBox(align="left")
    hbar1.add(empty_selbox, levelmap)
    levelchange.add(hbar1)

    # the make level state
    levelmake = gui.Container(width=1280, height=768)
    save_button = gui.Button('save')
    save_button.connect(CLICK, levelmaker.saveLevel()) 
    back_button = gui.Button('change level')
    obj_selbox = gui.SelectBox(width=256)
    left_vbar = gui.VBox(align="left", valign="top", spacing=5)
    left_vbar.add(save_button, back_button, obj_selbox)
    levelmake.add(left_vbar)

    # now add them to the main container
    menus.add(levelchange, levelmake)
    back_button.connect(CLICK, levelchoser.chooseLevel())


    # activate the choose level state
    levelchoser.chooseLevel()

    running = True
    while running:
        clock.tick(35)
        events = pygame.event.get()

        for event in events:
            if event.type == QUIT:
                running = False

        app.run(events)
        app.draw()

        gui.update_display()




if __name__ == '__main__':
    main()








