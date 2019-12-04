import pygame
from tkinter import *
import numpy as np

import json

#import auth
from scenario import *
from object import *

running = True
game = None

obstacle_types = []
formations = []

with open("data/obstacles.json", "r") as f:
    obstacles = json.load(f)
    for o in obstacles["OBJECTS"]:
        obstacle_types.append(o)
    for p in obstacles["FORMATIONS"]:
        formations.append(p)

while running:

    #-----------------
    #Options Screen Loop
    #-----------------

    #Note: This must be at the top of the 'while running' loop, as pygame must be exited for tkinter to load.

    if game is not None: #So that this loop only runs the second loop around
        if game.get_status() == "Options":
            game.on_quit()

            opt = Tk()
            #https://grokbase.com/t/python/python-win32/10c21rbqp0/prevent-a-tkinter-window-from-maximizing-via-win32-api-call
            opt.wm_resizable(False, False)            
            opt.geometry("250x200")
            opt.title("Options")

            back = Button(text="Back", command=opt.destroy)
            back.place(x=10, y=10)

            opt.mainloop()

    #-------------------------------------------
    #TITLE SCREEN
    #-------------------------------------------

    #Create a display window
    dim = dw, dh = 500, 500 #Display's width and height

    game = Game("Title", 200, 200, 60)
    red, green, blue, white, black = game.get_colours()

    obh = game.get_obh()

    #Fonts
    menu_font = pygame.font.SysFont(name='Bahnschrift', size=15, bold=False, italic=False)

    #TextObjects
    button1_text = TextObject("Play", menu_font, black)
    button2_text = TextObject("Options", menu_font, black)
    button3_text = TextObject("Quit", menu_font, black)

    #Buttons
    button1 = UI((0, 30, 100, 20), red, "TITLE_PLAY", button1_text)
    button2 = UI((0, 60, 100, 20), green, "TITLE_OPTIONS", button2_text)
    button3 = UI((0, 90, 100, 20), blue, "QUIT", button3_text)

    #Title functions
    obh.add_object(button1)
    obh.add_ui(button1)

    obh.add_object(button2)
    obh.add_ui(button2)

    obh.add_object(button3)
    obh.add_ui(button3)

    button1.set_axis_to_centre('x')
    button2.set_axis_to_centre('x')
    button3.set_axis_to_centre('x')

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

    #Create the score counter

    score_counter = TextObject("0", menu_font, red)

    score = UI((0, 100, 100, 100), black, None, score_counter)

    obh.add_object(score)
    obh.add_ui(score)
    obh.set_score_counter(score)

    #Create the obstacles

    #obstacle = Object((600, 350, 200, 10), blue)

    #obh.add_object(obstacle)
    #obh.add_moving(obstacle)
    #obh.add_ground(obstacle)

    #obstacle2 = Object((800, 275, 200, 10), red)

    #obh.add_object(obstacle2)
    #obh.add_moving(obstacle2)
    #obh.add_ground(obstacle2)

    #obstacle3 = Object((1000, 200, 200, 10), white)

    #obh.add_object(obstacle3)
    #obh.add_moving(obstacle3)
    #obh.add_ground(obstacle3)

    floor.set_axis_to_centre('x')

    #Game Loop
    #-----------------
    while game.get_status() == "Game":
        game.on_execute()
    #-----------------
