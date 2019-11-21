import pygame
import numpy as np

import auth
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


game = Game("Authorisation", 200, 200, 60)

#Fonts
menu_font = pygame.font.SysFont(name='Bahnschrift', size=15, bold=False, italic=False)

#TextObjects
button1_text = TextObject("Play", menu_font, black)

#Buttons
button1 = UI((0, 30, 100, 20), red, 1, "TITLE_PLAY", button1_text)

#Title functions
game.add_object(button1)
game.add_button(button1)

button1.set_centre_to_centre_of_surface('x')

while True:
    game.on_execute()

    if game.get_title() == "Game":
        #Create the player object
        player = Player((100, 100, 100, 100), red, 1)
        game.add_object(player)
        game.set_player(player)

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
