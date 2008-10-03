#
# menucontrol.py
#

import os
import sys

# makes importing of modules in lib directory possible
sys.path.insert(0, os.path.join("lib")) 

from gameinstances import *
from gamefunc import *
from events import *

class MenuController:
    '''
    manages the menu-system
    '''
    def __init__(self, mediator, container):
        self.mediator = mediator
        self.mediator.addObserver('inputwaiters', self)
        self.container = container
        self.mainmenu = {'new game':"self.mediator.inform('levelcontrol', NewGame())",\
                'options':'self.fillMenu(self.optionsmenu)',\
                'quit':"self.mediator.inform('inputwaiters', Quit())"}
        self.optionsmenu = {'sound':"self.mediator.inform('inputwaiters', Quit())",\
                'display':"self.mediator.inform('inputwaiters', Quit())",\
                'back':'self.fillMenu(self.mainmenu)'}
        self.menu = []

    def fillMenu(self, menu):
        '''
        draws a menu on the screen
        '''
        self.menu = []
        self.container.menuSprites.remove() # clear previous menu
        pos = (300,300)
        for name, callback in menu.iteritems():
            self.menu.append(menuButton(name, callback, pos))
            pos = (pos[0], pos[1] + 30)
        self.container.menuSprites.add(self.menu)
        self.activebutton = 0
        self.menu[self.activebutton].activate()

    def navUp(self):
        self.menu[self.activebutton].deactivate()
        self.activebutton -= 1
        try:
            self.menu[self.activebutton].activate()
        except IndexError:
            self.activebutton = -1
            self.menu[self.activebutton].activate()

    def navDown(self):
        self.menu[self.activebutton].deactivate()
        self.activebutton += 1
        try:
            self.menu[self.activebutton].activate()
        except IndexError:
            self.activebutton = 0
            self.menu[self.activebutton].activate()

    def navEnter(self):
        eval(self.menu[self.activebutton].callback)

    def navBack(self):
        self.fillMenu(self.mainmenu)
        

    def inform(self, event):
        if event.name == 'ChangeState':
            if event.state == 'menu':
                self.fillMenu(self.mainmenu)
        elif event.name == 'MenuNav':
            if event.navigation == 'up':
                self.navUp()
            if event.navigation == 'down':
                self.navDown()
            if event.navigation == 'enter':
                self.navEnter()
            if event.navigation == 'back':
                self.navBack()


