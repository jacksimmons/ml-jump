import pygame
from pygame.locals import *

from object import *
from object_handler import ObjectHandler
from colour import Colour
#TextObject, Object, Player, UI, Obstacle

class Game:
    "The master class - controls the ObjectHandler"
    #Source tutorial: http://pygametutorials.wikidot.com/tutorials-basic
    def __init__(self, title):

        #Window Variables
        self.__title: str = title
        self.__size: tuple = (1280, 720)

        #Pygame initialisation
        self.on_init()

        #Pygame variables
        self.__surface: pygame.Surface = pygame.display.set_mode(self.__size, pygame.HWSURFACE | pygame.DOUBLEBUF, 0, 0, 1)
        self.__clock: pygame.time.Clock = pygame.time.Clock()

        #Status variables
        self.__is_running = True
        self.__menu = "Title"
        self.__hovering = False
        self.__paused = False
        self.__globalCounter = 0

        #Jumping variables
        self.__jumping = False
        self.__jump_counter = 0

        #Object Handler
        self.__obh = ObjectHandler() #ObjectHandler object

        #Other variables
        # self.yd_font = pygame.font.SysFont(name='Bahnschrift', size=30, bold=False, italic=False)
        self.new_scene("Title")

    def on_init(self):
        pygame.init()
        pygame.display.set_caption(self.get_title())

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.__is_running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            name = self.__obh.check_hovering(x, y, True)

            if name != False:
                #Buttons on the Title Screen
                if name == 'TITLE_AI':
                    self.new_scene("AI")
                    self.__menu = "AI"
                elif name == 'TITLE_PLAY':
                    self.new_scene("Game")
                    self.__menu = "Game"

                    #Create the player
                    player = Object((100, 650, 20, 20), Colour.red)
                    self.__obh.add_object(player)
                    self.__obh.set_player(player)

                    #Create the floor
                    floor = Object((0, 700, 1280, 30), Colour.green)
                    floor.set_axis_to_centre('x')
                    floor.set_axis_centre('y', 715)

                    self.__obh.add_ground(floor)
                    self.__obh.set_floor(floor)

                    #Create the debug stat UI elements
                    menu_font = pygame.font.SysFont(name='Bahnschrift', size=15, bold=False, italic=False)

                    player_pos_text = TextObject("Player Rect: (0, 0, 0, 0)", menu_font, Colour.red)
                    player_pos_ui = UI((0, 0, 100, 10), Colour.black, None, player_pos_text)

                    self.__obh.add_ui(player_pos_ui)
                    self.__obh.set_player_pos_disp(player_pos_ui)

                    player_grounded_text = TextObject("Player Ground Status: ", menu_font, Colour.red)
                    player_grounded_ui = UI((0, 20, 100, 10), Colour.black, None, player_grounded_text)

                    self.__obh.add_ui(player_grounded_ui)
                    self.__obh.set_player_grounded_disp(player_grounded_ui)

                    tplayer_f_cnt = TextObject("Player Floored Counter: ", menu_font, Colour.green)
                    player_f_cnt = UI((0, 40, 100, 10), Colour.black, None, tplayer_f_cnt)

                    self.__obh.add_ui(player_f_cnt)
                    self.__obh.set_player_floored_cnt_disp(player_f_cnt)

                    score_counter = TextObject("Score: 0", menu_font, Colour.red)
                    score = UI((0, 60, 100, 10), Colour.black, None, score_counter)

                    self.__obh.add_ui(score)
                    self.__obh.set_score_counter(score)

                elif name == 'TITLE_OPTIONS':
                    self.__menu = "Options"
                elif name == 'MAIN_MENU':
                    self.__menu = "Title"
                elif name == 'QUIT':
                    self.__is_running = False

        if event.type == pygame.KEYDOWN:
            if self.__menu == "Game":
                if event.key == pygame.K_SPACE:
                    self.__jumping = True
                if event.key == pygame.K_ESCAPE:
                    self.__paused = not self.__paused

        if event.type == pygame.KEYUP:
            if self.__menu == "Game":
                if event.key == pygame.K_SPACE:
                    self.__jumping = False

    def on_loop(self):
        "The standard loop method where all object and physics handling is done"
        if self.__jumping:
            if self.__jump_counter > 0:
                self.__jump_counter -= 1
            else:
                jumped = self.__obh.handle_jumping(True)
                if jumped:
                    self.__jump_counter = 1
        else:
            self.__jump_counter = 0
            
        self.__obh.handle_objects()
        self.__obh.generate_ground(self.__globalCounter)
        
        self.__clock.tick(self.__fps_lim)

        game = self.__obh.handle_obstacles()

        if game == False:
            self.new_scene("You Died", self.__size, 60, False)

    def on_render(self):
        "Render any valid objects"
        self.__surface.fill(Colour.black)
        self.__obh.render(self.__surface)

    def on_quit(self):
        "Exit the game; close the program"
        pygame.quit()

    def on_execute(self, paused:bool=False):
        "The gameloop; run events, run the loop, render objects and check if the program should close."
        if self.__is_running:
            for event in pygame.event.get():
                self.on_event(event)
            if self.__paused:
                self.__globalCounter += 1
            else:
                self.on_loop()
                self.on_render()
        else:
            self.on_quit()

    def get_title(self):
        "Return the Window name"
        return self.__title

    def get_menu(self):
        "Return the game's status"
        return self.__menu

    def new_scene(self, title, size:tuple=(1280, 720), fps_limit:int=60, custom_status=False):
        """Create a new scene. This edits the existing window by
changing the title, dimensions and FPS limit, and resetting all existing
objects."""
        self.__title = title
        self.__size = self.__width, self.__height = size
        self.__is_running = True
        self.__fps_lim = fps_limit

        if custom_status == False:
            self.__menu = self.__title
        else:
            self.__menu = custom_status

        self.surface = pygame.display.set_mode(self.__size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption(self.__title)

        self.__obh.cleanup()

    def get_obh(self):
        "Return the ObjectHandler object associated with the Game"
        return self.__obh
