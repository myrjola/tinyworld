# 
# File: levelmaker3.py
# Author: Martin Yrjola
# Desc: A levelmaker for the platformer 
#       Will be of great help when making
#       the game. now trying with qt
#
import pygame
import sys
import os
import pickle
from pygame.locals import *

from PyQt4 import QtGui, QtCore

class MainWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setWindowTitle('LevelMaker')
        self.layoutInit()
        self.qActions()
        self.objectList()
        self.resize(1200, 800)

    def layoutInit(self):
        self.hbox = QtGui.QHBoxLayout()
        self.hbox.addStretch(1)
        self.setLayout(self.hbox)

    def qActions(self):
        self.exit = QtGui.QAction(QtGui.QIcon('levelmaker/pixmaps/exit.png'), 'Exit', self)
        self.exit.setShortcut('Ctrl+Q')
        self.connect(self.exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

    def graphicsArea(self):
        self.graphview = QtGui.QGraphicsView()
        self.hbox.addWidget(self.graphview)

    def objectList(self):
        self.objlist = QtGui.QListView()
        self.hbox.addWidget(self.objlist)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

