########### The Mediator ###################

class Mediator:
    '''
    A base class to send events to other
    objects.

    '''
    def __init__(self):
        self.observers = []
        self.event_queue  = []
    def addObserver(self, observer):
        self.observers.append(observer)
    def delObserver(self, observer):
        self.observers.remove(observer)
        del(observer)
    def inform(self, event):
        # Sends an event to all observers
        for observer in self.observers:
            observer.inform(event)


