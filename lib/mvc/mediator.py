########### The Mediator ###################

class Mediator:
    '''
    A base class to send events to other
    objects.

    '''
    def __init__(self):
        self.observers = {'others':[], 'tickwaiters':[], 'inputwaiters':[]}

    def addObserver(self, name = 'others', observer = None):
        if name == 'tickwaiters':
            self.observers[name].append(observer)
        elif name == 'inputwaiters':
            self.observers[name].append(observer)
        elif name == 'others':
                self.observers[name].append(observer)
        else:
            self.observers[name] = observer

    def delObserver(self, observer):
        self.observers.remove(observer)
        del(observer)

    def inform(self, toWhom = 'others', event = None):
        # Sends an event to toWhom
        if toWhom == 'tickwaiters':
            for observer in self.observers['tickwaiters']:
                observer.inform(event)
        elif toWhom == 'inputwaiters':
            for observer in self.observers['inputwaiters']:
                observer.inform(event)
        elif toWhom == 'others':
            for observer in self.observers['others']:
                observer.inform(event)
        else: self.observers[toWhom].inform(event)


