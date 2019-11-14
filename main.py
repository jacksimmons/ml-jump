import pygame
import numpy as np
from scenario import Scenario

#Initialise pygame
pygame.init()

scenario = Scenario()

#Create a display window
dim = dw, dh = 500, 500 #Display's width and height

splitx = 100 #The x coordinate of the line separating the main window and the dev console

disp = pygame.display.set_mode(dim)
pygame.display.set_caption("Title Screen")

#Initialise fonts
font = pygame.font.SysFont('Bahnschrift', 30)

x = 50
y = 50
w = 50
h = 50

v = 5

black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255

#Create a Clock object and limit framerate
clock = pygame.time.Clock()
fps_limit = 60

#Titlescreen loop
title = True

def adjust_to_centre_x(rect, dim):
  x, y, w, h = rect[0], rect[1], rect[2], rect[3]
  newx = dim[0]/2 - w/2
  return (newx, y, w, h)


while title:
    events()
    loop()
    render()
    
    clock.tick(fps_limit)
  
    #Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            title = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        y -= v

    print(clock.get_time())

    disp.fill(black)
    title1 = pygame.draw.rect(disp, red, adjust_to_centre_x(rects['b1'], dim))
    r = font.render('Text', False, black)
    disp.blit(r, title1)
    pygame.display.update()

pygame.quit()
