import pygame
import numpy as np
from scenario import *

#Initialise pygame
pygame.init()

#Constants
g = -9.8

#Variables
movement = [] # A list of (direction, magnitude)

#Create a display window
dim = dw, dh = 500, 500 #Display's width and height

splitx = 100 #The x coordinate of the line separating the main window and the dev console

#Initialise fonts

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

#Titlescreen loop
title = True

def adjust_to_centre_x(x, w):
  newx = dim[0]/2 - w/2
  return x, w

def physics_update(scenario):
    scenario.append_dynamic(player)
    objects = scenario.get_dynamic()


def events(player):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            title = False

        elif event.type == pygame.KEYDOWN:

            x, y = 0, 0

            global movement

            if event.key == pygame.K_w:
                movement.append(('y', -v))
            elif event.key == pygame.K_a:
                movement.append(('x', -v))
            elif event.key == pygame.K_s:
                movement.append(('y', v))
            elif event.key == pygame.K_d:
                movement.append(('x', v))

        elif event.type == pygame.KEYUP:

            if event.key == pygame.K_w:
                movement.remove(('y', -v))
            elif event.key == pygame.K_a:
                movement.remove(('x', -v))
            elif event.key == pygame.K_s:
                movement.remove(('y', v))
            elif event.key == pygame.K_d:
                movement.remove(('x', v))

def loop(player):

    global movement

    for move in movement:
        player.move(move[0], move[1])

title = Scene("Title Screen", 500, 500, 60)

menu_font = pygame.font.SysFont(name='Bahnschrift', size=15, bold=False, italic=False)
button1_text = TextObject("Play", menu_font, black)
button1 = UI(1, (0, 30, 100, 20), red, 1, 0, None, button1_text)

title.add_object(button1)
title.add_button(button1)

button1.set_centre_to_centre_of_surface('x')

title.on_execute()

    #physics_update(scenario)
    #events(player)
    #loop(player)
    #render()

    #clock.tick(fps_limit)
    #
    #disp.fill(black)
    #title1 = pygame.draw.rect(disp, red, (20, 20, 20, 20))
    #r = font.render('Text', False, black)
    #disp.blit(r, title1)
    #pygame.draw.rect(disp, red, player.get_rect())
    #pygame.display.update()


#player_rect = (50, 50, 50, 50)
#player = Object(0, player_rect, red)

pygame.quit()
