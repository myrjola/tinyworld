########### The Events ######################

class Tick:
    def __init__(self):
        self.name = "Tick"

class InGameTick(Tick):
    def __init__(self):
        Tick.__init__(self)
        self.tickname = "InGameTick"

class MenuTick(Tick):
    def __init__(self):
        Tick.__init__(self)
        self.tickname = "MenuTick"

class PauseTick(Tick):
    def __init__(self):
        self.tickname = "PauseTick"

class Quit:
    def __init__(self):
        self.name = "Quit"

class MoveChar:
    def __init__(self, direction):
        self.name = "MoveChar"
        self.direction = direction 

class DisplayReady:
    def __init__(self):
        self.name = "DisplayReady"

class LevelChange:
    def __init__(self, x, y):
        self.name = "LevelChange"
        self.left_or_right = x
        self.up_or_down = y



