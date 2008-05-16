####################
#gamefunc.py
#module including useful functions
#for a game.
#####################
import pygame, os

def imgLoad(imgname):
	'''Load image and return image object'''
	whole_path = os.path.join('images',imgname)
	try: 
		img = pygame.image.load(whole_path)
		if img.get_alpha():
			img = img.convert_alpha()
		else:
			img = img.convert()
	
	except pygame.error, message:
		print 'Image not found: ', whole_path
		raise SystemExit, message
	return img, img.get_rect()



	
