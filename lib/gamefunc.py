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


def imgListMake(imgname, frames):
    '''Load image sheet and split into imagelist'''
    imglist = []
    img, imgrect = imgLoad(imgname) 
    size = ((imgrect.width / frames), (imgrect.height))
    offset = (0,0)
    tmpimg = pygame.Surface(size)
    for i in range(0, frames - 1):
        tmpimg.blit(img, (0,0), (offset, size))
        imglist.append(tmpimg)
        offset = ((offset[0] + size[0]), offset[1])
    return imglist

def aniDictMake(sprname, aninames, anilengths):
    '''Creates the complete dictionary of a sprites animations
       aninames = list with the names of animation ie. walk, jump...'''
    anidict = {}
    for aniname, anilenght in aninames, anilengths:
        filename = sprname + '_' + aniname
        anidict[aniname] = imgListMake(filename, anilenght) 
    return anidict
    
