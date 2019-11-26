import pygame
import numpy as np

#import auth
from scenario import *
from object import *

#-------------------------------------------
#TITLE SCREEN
#-------------------------------------------

#Create a display window
dim = dw, dh = 500, 500 #Display's width and height

game = Game("Authorisation", 200, 200, 60)
red, green, blue, white, black = game.get_colours()

obh = game.get_obh()

#Fonts
menu_font = pygame.font.SysFont(name='Bahnschrift', size=15, bold=False, italic=False)

#TextObjects
button1_text = TextObject("Play", menu_font, black)

#Buttons
button1 = UI((0, 30, 100, 20), red, "TITLE_PLAY", button1_text)

#Title functions
obh.add_object(button1)
obh.add_ui(button1)

button1.set_axis_to_centre('x')

#Title Screen Loop
#-----------------
while game.get_status() == "Title":
    game.on_execute()
#-----------------

#-------------------------------------------
#GAME
#-------------------------------------------

#Create the player object

player = Object((100, 300, 20, 20), red)

obh.add_object(player)
obh.set_player(player)

#Create the floor

floor = Object((0, 400, 600, 10), green)

obh.add_object(floor)
obh.add_ground(floor)

#Create the obstacles

obstacle = Object((600, 350, 200, 10), blue)

obh.add_object(obstacle)
obh.add_moving(obstacle)
obh.add_ground(obstacle)

obstacle2 = Object((800, 275, 200, 10), red)

obh.add_object(obstacle2)
obh.add_moving(obstacle2)
obh.add_ground(obstacle2)

obstacle3 = Object((1000, 200, 200, 10), white)

obh.add_object(obstacle3)
obh.add_moving(obstacle3)
obh.add_ground(obstacle3)

floor.set_axis_to_centre('x')

#Game Loop
#-----------------
while game.get_status() == "Game":
    game.on_execute()
#-----------------
