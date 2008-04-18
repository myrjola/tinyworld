'''
New try on the platformer without using MVC and mediator
'''
import math, os, sys, pygame
from pygame.locals import *

sys.path.insert(0, os.path.join("lib")) 
from objects import *

def main():
	pygame.init()
	screen = pygame.display.set_mode([1024,768])
	spritegroup = pygame.sprite.RenderUpdates()
	player = mainChar1([400,200])
	ball = bounceBall([1,5],[400,200])
	spritegroup.add(player, ball)
	background = pygame.Surface([1024,768])
	background.fill([255,255,255])
	screen.blit(background, [0,0])
	pygame.display.flip()
	clock = pygame.time.Clock()
	while 1:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == QUIT:
				return
			elif event.type == KEYDOWN:
				if event.key == K_UP:
					print "jump"
					player.Move("jump")

				if event.key == K_DOWN:
					player.Move("duck")

				if event.key == K_LEFT:
					player.Move("left")

				if event.key == K_RIGHT:
					player.Move("right")

		spritegroup.update()
		rectlist = spritegroup.draw(screen)
		pygame.display.update(rectlist)
		spritegroup.clear(screen,background)
		

if __name__ == '__main__': main()	
	

