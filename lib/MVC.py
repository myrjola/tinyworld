#######################
#MVC.py
#My first try to implement a Model-View-Controller
#Many thing stolen from sjbrowns tutorial
###################3

class Event:
	"""event superclass"""
	def __init__(self):
		self.name = "Generic Event"

class TickEvent(Event):
	def __init__(self):
		self.name = "CPU Tick Event"

class QuitEvent(Event):
	def __init__(self):
		self.name = "Program Quit Event"
class GameStartedEvent(Event):
	def __init__(self, game):
		self.name = "Game Started Event"
		self.game = game
class CharactorMoveRequest(Event):
	def __init__(self, charactor):
		self.name = "Charactor Move Event"
		self.direction = direction

class EventManager:
	"""The mediator betveen MVC"""
	def __init__(self):
		from weakref import WeakKeyDictionary
		self.listeners = WeakKeyDictionary()
		self.eventQueue = []

	def RegisterListener(self, listener):
		self.listeners[ listener ] = 1
	
	def UnregisterListener(self, listener):
		if listener in self.listeners.keys():
			del self.listeners[ listener ]
	
	def Post(self, event):
		for listener in self.listeners.keys():
			#NOTE: If the weakref has died it will
			#be automatically removed, so we don't
			#have to worry about it
			listener.Notify(event)
	
	def Notify(self, event):
		if not isinstance(event, TickEvent): Debug("	Message: " +
				event.name)
		for listener in self.listeners.keys():
			#If weakref has died, remove it and continue
			#through the list
			if listener is None:
				del self.listeners[listener]
				continue
			listener.Notify(event)


class KeyboardController:
	def Notify(self, event):
		if isinstance( event, TickEvent ):
			#TODO: Handle input events
			for event in pygame.event.get():
				ev = None
				if event.type == QUIT:
					ev = QuitEvent()
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						ev = QuitEvent
					elif event.key == K_UP:
						ev = CharactorMoveRequest('jump')
					elif event.key == K_DOWN:
						ev = CharactorMoveRequest('duck')
					elif event.key == K_LEFT:
						ev = CharactorMoveRequest('left')
					elif event.key == K_UP:
						ev = CharactorMoveRequest('right')
				if ev:
					self.evManager.Notify( ev )
	
	


class CPUSpinnerController:
	def __init__(self):
		#implement fps-limit
		self.clock = pygame.time.Clock()

	def Run(self):
		while self.keepGoing:
			self.clock.tick(60)
			event = TickEvent()
			self.evManager.Post(event)

	def Notify(self,event):
		if isinstance(event,QuitEvent):
			#stop the while loop
			self.keepGoing = 0

class PygameView:
	def __init__(self):
		self.evManager = evManager
		self.evManager.RegisterListener( self )


		screen = pygame.display.set_mode([800,400])
		
	def Notify(self, event):
		if isinstance( event, TickEvent ):
			#TODO; draw everything
			


