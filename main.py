import pygame
from tkinter import *

from scenario import *
from object import *

running = True
game = None

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

    if game is None or (game is not None and game.get_status() == "Title"):
        #Create a display window
        dim = dw, dh = 500, 500 #Display's width and height

        game = Game("Title", 1920, 200, 60)
        red, yellow, green, cyan, blue, magenta, white, black = game.get_colours()

        obh = game.get_obh()

        #Fonts
        menu_font = pygame.font.SysFont(name='Bahnschrift', size=15, bold=False, italic=False)
        menu_font_large = pygame.font.SysFont(name='Bahnschrift', size=50, bold=False, italic=False)

        #TextObjects
        button0_text = TextObject("AI", menu_font, black)
        button1_text = TextObject("Play", menu_font, black)
        button2_text = TextObject("Options", menu_font, black)
        button3_text = TextObject("Quit", menu_font, black)

        #Buttons
        button0 = UI((0, 30, 100, 20), magenta, "TITLE_AI", button0_text)
        button1 = UI((0, 60, 100, 20), red, "TITLE_PLAY", button1_text)
        button2 = UI((0, 90, 100, 20), green, "TITLE_OPTIONS", button2_text)
        button3 = UI((0, 120, 100, 20), blue, "QUIT", button3_text)

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
        while game.get_status() == "Title":
            game.on_execute()
        #-----------------

    #-------------------------------------------
    #GAME
    #-------------------------------------------

    #Create the player object

    player = Object((100, 650, 20, 20), red)

    obh.add_object(player)
    obh.set_player(player)

    #Create the floor

    floor = Object((0, 700, 1280, 30), green)

    obh.add_object(floor)
    obh.add_ground(floor)
    obh.set_floor(floor)
    floor.set_axis_to_centre('x')
    floor.set_axis_centre('y', 715)

    #Create the debug stat UI elements

    tplayer_pos = TextObject("Player Rect: (0, 0, 0, 0)", menu_font, red)
    player_pos = UI((0, 0, 100, 10), black, None, tplayer_pos)

    obh.add_object(player_pos)
    obh.add_ui(player_pos)
    obh.set_player_pos_disp(player_pos)

    tplayer_grounded = TextObject("Player Ground Status: ", menu_font, red)
    player_grounded = UI((0, 20, 100, 10), black, None, tplayer_grounded)

    obh.add_object(player_grounded)
    obh.add_ui(player_grounded)
    obh.set_player_grounded_disp(player_grounded)

    tplayer_f_cnt = TextObject("Player Floored Counter: ", menu_font, green)
    player_f_cnt = UI((0, 40, 100, 10), black, None, tplayer_f_cnt)

    obh.add_object(player_f_cnt)
    obh.add_ui(player_f_cnt)
    obh.set_player_floored_cnt_disp(player_f_cnt)

    score_counter = TextObject("Score: 0", menu_font, red)
    score = UI((0, 60, 100, 10), black, None, score_counter)

    obh.add_object(score)
    obh.add_ui(score)
    obh.set_score_counter(score)

    #Game Loop
    #-----------------
    while game.get_status() == "Game":
        game.on_execute()
    #-----------------

    you_died = TextObject("You Died...", menu_font_large, red)
    yd_ui = UI((0, 100, 0, 0), black, None, you_died)
    yd_ui.set_axis_centre('x', 550)
    obh.add_object(yd_ui)
    obh.add_ui(yd_ui)

    yd_continue_text = TextObject("Continue", menu_font, black)
    yd_continue = UI((0, 300, 100, 20), green, "TITLE_PLAY", yd_continue_text)
    yd_continue.set_axis_centre('x', 600)

    obh.add_object(yd_continue)
    obh.add_ui(yd_continue)

    yd_quit_text = TextObject("Quit", menu_font, black)
    yd_quit = UI((0, 300, 100, 20), red, "QUIT", yd_quit_text)
    yd_quit.set_axis_centre('x', 700)

    yd_menu_text = TextObject("Main Menu", menu_font, black)
    yd_menu = UI((0, 350, 100, 20), blue, "MAIN_MENU", yd_menu_text)
    yd_menu.set_axis_centre('x', 600)

    obh.add_object(yd_quit)
    obh.add_ui(yd_quit)

    obh.add_object(yd_menu)
    obh.add_ui(yd_menu)

    #Death Loop
    #-----------------
    while game.get_status() == "You Died":
        game.on_execute()
    #-----------------

    #-------------------------------------------
    #Machine Learning Mode
    #-------------------------------------------

    #ML Game Loop
    #-----------------

    while game.get_status() == "AI":
        game.on_execute()
    #-----------------
