########### Container ######################

class Container:
    ''' 
    Contains information needed by many
    game objects in the middle of the
    game ie. list of walls for collision-
    detection, time taken for one frame,
    etc...
    '''
    def __init__(self, mediator):
        self.mediator = mediator
        self.mediator.addObserver('container', self)
        self.solidwalls = []    # used for collision detection
        self.screen = 0
        self.background = 0     # the background-image and platforms reside here
        self.badGuysSprites = 0     # the enemies
        self.goodGuysSprites = 0    # the friends
        self.mainchar = 0           # hmm... what could this be
        self.maincharalive = 0 

    def inform(self, event):
        # still nothing implemented, maybe in the future...
        pass


