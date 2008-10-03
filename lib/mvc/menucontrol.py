class MenuController:
    '''
    manages the menu-system
    '''
    def __init__(self, mediator, container):
        self.mediator = mediator
        self.mediator.addObserver(self)
        self.container = container
        self.mainmenu = []
        self.optionsmenu = []

    def inform(self, event):


