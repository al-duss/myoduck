import pygame

def	pictures_path(file):
	surface = pygame.image.load("assets/" + file)
	return surface

background_colour = (255,255,255)
(width, height) = (300, 200)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tutorial 1')
screen.fill(background_colour)
img = pictures_path("square.png")
imgx=0
imgy=20
dist = 0
direction = 1
screen.blit(img, (imgx, imgy))
pygame.display.flip()
FPS = 30
fpsTime = pygame.time.Clock()
running = True
#while running:
  # if pygame.K_DOWN: # down key
  #   imgy += dist # move down
  # elif pygame.K_UP: # up key
  #   imgy -= dist # move up
  # if pygame.K_RIGHT: # right key
  #   imgx += dist # move right
  # elif pygame.K_LEFT: # left key
  #   imgx -= dist # move left
	# for event in pygame.event.get():
	# 	if 	(event.type == pygame.QUIT):
	# 		running = False
 #  		if 	(event.type == pygame.KEYDOWN):
 #  			if (event.key == pygame.K_LEFT):
 #  				dist =-1
 #  			if (event.key == pygame.K_RIGHT):
 #  				dist = 1
 #  		if (event.type == pygame.KEYUP):
 #  			if (event.key == pygame.K_LEFT):
 #  				dist = 0
 #  			if (event.key == pygame.K_RIGHT):
 #  				dist = 0
 #  	imgx += dist
	# screen.blit(img, (imgx, imgy))
 #  	pygame.display.update()
 #  	screen.fill(background_colour)
 #  	fpsTime.tick(FPS)
while running:
	if direction==1: 
		dist = 10
		imgx += direction*dist
		screen.blit(img, (imgx, imgy))
  		pygame.display.update()
  		screen.fill(background_colour)
  		fpsTime.tick(FPS)
  		if imgx >= 255:
  		  direction = -1

	if direction == -1:
		dist = 10
		imgx += direction*dist
		screen.blit(img, (imgx, imgy))
  		pygame.display.update()
  		screen.fill(background_colour)
  		fpsTime.tick(FPS)
  		if imgx <= 0:
  		  direction = 1
running=False




