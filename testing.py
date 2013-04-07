import pygame, sys,os,api,constants
from pygame.locals import * 
 
pygame.init() 
 
window = pygame.display.set_mode((468, 500)) 
screen = pygame.display.get_surface() 

i = j = 0

print(api.get_by_tag("apple"))
l = api.get_by_tag("horse")

for x in l:
  image = pygame.image.load(api.get_image(x), x)

  
  print("width {0}".format(image.get_width()))
  print("height {0}".format(image.get_height()))
  print("----")

  box_size = min(image.get_width(), image.get_height())
  new_image = pygame.Surface((box_size, box_size))
  new_image.blit(image, (0, 0))

  new_image = pygame.transform.scale(new_image, (128,128))

  screen.blit(new_image, (j*128,0)) 
  j += 1

border = pygame.Surface((128,128))
border.set_colorkey(constants.BLACK)
pygame.draw.lines(border,constants.RED, False, [(0,0),(127,0),(127,127),(1,127),(0,0)])
screen.blit(border,(0,0))
pygame.display.flip() 
 
while True: 
   input(pygame.event.get()) 
