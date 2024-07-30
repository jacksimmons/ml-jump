import pygame
from tkinter import *

from game import *
from object import *
from colour import Colour

running = True
game = None

while running:

    #-----------------
    #Options Screen Loop
    #-----------------

    #Note: This must be at the top of the 'while running' loop, as pygame must be exited for tkinter to load.

    if game is not None: #So that this loop only runs the second loop around
        if game.get_menu() == "Options":
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

    if game is None or (game is not None and game.get_menu() == "Title"):
        #Create a display window
        dim = dw, dh = 500, 500 #Display's width and height

        game = Game("Title")

        obh = game.get_obh()

        #Fonts
        menu_font = pygame.font.SysFont(name='Bahnschrift', size=15, bold=False, italic=False)
        menu_font_large = pygame.font.SysFont(name='Bahnschrift', size=50, bold=False, italic=False)

        #TextObjects
        button0_text = TextObject("AI", menu_font, Colour.black)
        button1_text = TextObject("Play", menu_font, Colour.black)
        button2_text = TextObject("Options", menu_font, Colour.black)
        button3_text = TextObject("Quit", menu_font, Colour.black)

        #Buttons
        button0 = UI((0, 30, 100, 20), Colour.magenta, "TITLE_AI", button0_text)
        button1 = UI((0, 60, 100, 20), Colour.red, "TITLE_PLAY", button1_text)
        button2 = UI((0, 90, 100, 20), Colour.green, "TITLE_OPTIONS", button2_text)
        button3 = UI((0, 120, 100, 20), Colour.blue, "QUIT", button3_text)

        #Title functions
        obh.add_object(button0)
        obh.add_ui(button0)

        obh.add_object(button1)
        obh.add_ui(button1)

        obh.add_object(button2)
        obh.add_ui(button2)

        obh.add_object(button3)
        obh.add_ui(button3)

        button0.set_axis_to_centre('x')
        button1.set_axis_to_centre('x')
        button2.set_axis_to_centre('x')
        button3.set_axis_to_centre('x')

        #Title Screen Loop
        #-----------------
        while game.get_menu() == "Title":
            game.on_execute()
        #-----------------

    #-------------------------------------------
    #GAME
    #-------------------------------------------

    #Game Loop
    #-----------------
    while game.get_menu() == "Game":
        game.on_execute()
    #-----------------

    you_died = TextObject("You Died...", menu_font_large, Colour.red)
    yd_ui = UI((0, 100, 0, 0), Colour.black, None, you_died)
    yd_ui.set_axis_centre('x', 550)
    obh.add_object(yd_ui)
    obh.add_ui(yd_ui)

    yd_continue_text = TextObject("Continue", menu_font, Colour.black)
    yd_continue = UI((0, 300, 100, 20), Colour.green, "TITLE_PLAY", yd_continue_text)
    yd_continue.set_axis_centre('x', 600)

    obh.add_object(yd_continue)
    obh.add_ui(yd_continue)

    yd_quit_text = TextObject("Quit", menu_font, Colour.black)
    yd_quit = UI((0, 300, 100, 20), Colour.red, "QUIT", yd_quit_text)
    yd_quit.set_axis_centre('x', 700)

    yd_menu_text = TextObject("Main Menu", menu_font, Colour.black)
    yd_menu = UI((0, 350, 100, 20), Colour.blue, "MAIN_MENU", yd_menu_text)
    yd_menu.set_axis_centre('x', 600)

    obh.add_object(yd_quit)
    obh.add_ui(yd_quit)

    obh.add_object(yd_menu)
    obh.add_ui(yd_menu)

    #Death Loop
    #-----------------
    while game.get_menu() == "You Died":
        game.on_execute()
    #-----------------

    #-------------------------------------------
    #Machine Learning Mode
    #-------------------------------------------

    #ML Game Loop
    #-----------------

    while game.get_menu() == "AI":
        game.on_execute()
    #-----------------
