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
    for i in range(frames):
        tmpimg.blit(img, (0,0), (offset, size))
        imglist.append(tmpimg.copy())
        print 'added image: ', imgname, " frame: ", i + 1
        offset = ((offset[0] + size[0]), offset[1])
    return imglist

def aniDictMake(sprname, aninames, anilengths):
    '''Creates the complete dictionary of a sprites animations
       aninames = list with the names of animation ie. walk, jump...'''
    anidict = {}
    i = 0
    for aniname in aninames:
        anilength = anilengths[i]
        i += 1
        filename = sprname + '_' + aniname + '.png'
        anidict[aniname] = imgListMake(filename, anilength) 
        print "added entry ", aniname, ' with length ', anilength, \
                ' to anidict'
    return anidict
    
