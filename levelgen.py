
import pygame, sys, os, pickle
from pygame.locals import *

#makes importing of modules in lib directory possible
sys.path.insert(0, os.path.join("lib")) 
from gamefunc import *

listorder = ["mainchar","badguys","balls","platforms","walls"]
spritelist = ["char2.png","badguy1.png","ball1.png","solid.png","wall.png"]
leveldatadict = {"mainchar":[],"badguys":[],"balls":[],"platforms":[],"walls":[]}
listorderindex = 0
charlist = []
badguylist = []
platflist = []
wallist = []
level = str(raw_input('which level name? --> '))


pygame.init()
screen = pygame.display.set_mode([1024,768])
background = pygame.Surface([1024,768])
background.fill([255,255,255])
screen.blit(background,[0,0])
pygame.display.flip()
running = 1
objsprites = pygame.sprite.Group()
mousesprite = pygame.sprite.RenderUpdates()

class mouseSprite(pygame.sprite.Sprite):
    def __init__(self, (image,rect)):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = image,rect
    def update(self, image=None):
        self.rect.topleft = mousepos
        if image:
            self.image = image


class imgOfObject(pygame.sprite.Sprite):
    def __init__(self, (image,rect), pos):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = image,rect
        self.rect.topleft = pos

def alignToGrid((x,y)):
    #makes use of pythons way of rounding to integers
    xout = x/32*32
    yout = y/32*32
    return (xout,yout)
imgrect = load_png(spritelist[listorderindex])
mousesprite.add(mouseSprite(imgrect))

while running == 1:
    if pygame.mouse.get_focused:
        mousepos = alignToGrid(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == QUIT:
                running = 0
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    level = str(pygame.mouse.get_pos()[0]/64) + \
                            str(pygame.mouse.get_pos()[1]/64) 
                    print "You chose: ", level
                    running = 0
 
running = 1

while running == 1:
    if pygame.mouse.get_focused:
        mousepos = alignToGrid(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == QUIT:
                running = 0
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mousepos = alignToGrid(pygame.mouse.get_pos())
                    leveldatadict[listorder[listorderindex]].append(mousepos)
                    background.blit(imgOfObject(imgrect,mousepos).image, mousepos)
#                    objsprites.add(imgOfObject(imgrect,mousepos))
                if event.button == 3:
                    listorderindex += 1
                    try: 
                        print listorder[listorderindex]
                        imgrect = load_png(spritelist[listorderindex])
                        mousesprite.update(imgrect[0])
                    except IndexError: 
                        listorderindex = 1
                        imgrect = load_png(spritelist[listorderindex])
                        mousesprite.update(imgrect[0])


                print event.button
                print pygame.mouse.get_pos()
    mousesprite.update()
    objsprites.draw(background)
    screen.blit(background,(0,0))
    pygame.display.update(mousesprite.draw(screen))
print leveldatadict


#TODO make mouse driven level editor


'''
charlist.append([400,200])
badguylist.append([400,200])
platformlist = [[390,600],[390,300],[390,390]]
wallist = [[390,300],[700,300]]
'''


fullname = os.path.join('levels',level)
levelfile = open(fullname, 'w')
pickle.dump(leveldatadict, levelfile)
print "level generated"


