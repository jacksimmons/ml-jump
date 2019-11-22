import pygame
import numpy as np

#import auth
from scenario import *
from object import *

#Create a display window
dim = dw, dh = 500, 500 #Display's width and height

game = Game("Authorisation", 200, 200, 60)
red, green, blue, white, black = game.get_colours()

#Fonts
menu_font = pygame.font.SysFont(name='Bahnschrift', size=15, bold=False, italic=False)

#TextObjects
button1_text = TextObject("Play", menu_font, black)

#Buttons
button1 = UI((0, 30, 100, 20), red, "TITLE_PLAY", button1_text)

#Title functions
game.add_object(button1)
game.add_button(button1)

button1.set_axis_to_centre('x')

while game.get_status() == "Title":
    game.on_execute()

#Create the player object

player = Player((100, 300, 100, 100), red)

game.add_object(player)
game.set_player(player)
game.add_dynamic(player)

#Create the floor

floor = Object((0, 400, 600, 10), green)

game.add_object(floor)
game.add_ground(floor)

floor.set_axis_to_centre('x')

while game.get_status() == "Game":
    game.on_execute()
