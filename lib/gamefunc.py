####################
#gamefunc.py
#library including useful functions
#for a game.
#####################

def load_png(name):
	""Load image and return image object""
	fullname = os.path.join('image',name)
	try: 
		image = pygame.image.load(fullname)
		if image.get_alpha() is None:
			image = image.convert()
		else:
			image = image.convert_alpha()
	
	except pygame.error, message:
		print 'Cannot load image: ', fullname
		raise SystemExit, message
	return image, image.get_rect()



	
