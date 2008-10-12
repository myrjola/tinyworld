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
        Tick.__init__(self)
        self.tickname = "PauseTick"

class ChangeState:
    def __init__(self, state):
        self.name = "ChangeState"
        self.state = state

class Quit:
    def __init__(self):
        self.name = "Quit"

class MoveChar:
    def __init__(self, direction):
        self.name = "MoveChar"
        self.direction = direction 

class NewGame:
    def __init__(self):
        self.name = "NewGame"

class LevelChange:
    def __init__(self, x, y):
        self.name = "LevelChange"
        self.left_or_right = x
        self.up_or_down = y

class MenuNav:
    '''
    Navigate menu
    '''
    def __init__(self, navigation):
        self.name = "MenuNav"
        self.navigation = navigation

class ToPauseOrMenu:
    '''
    To inform the viewcontroller of gamestate change
    '''
    def __init__(self):
        self.name = "ToPauseOrMenu"

class ToInGame:
    def __init__(self):
        self.name = "ToInGame"

class MenuClear:
    def __init__(self):
        self.name = "MenuClear"

