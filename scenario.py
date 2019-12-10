import pygame
from pygame.locals import *

from object import *
#TextObject, Object, Player, UI, Obstacle

class Game:
    "The master class - controls the ObjectHandler"
    #Source tutorial: http://pygametutorials.wikidot.com/tutorials-basic
    def __init__(self, title, width, height, fps_lim):

        #Window Variables
        self.title = title
        self.size = self.width, self.height = width, height

        #Pygame initialisation
        self.on_init()

        #Pygame variables
        self.surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()

        #Status variables
        self.is_running = True
        self.status = "Title"
        self.fps_lim = fps_lim
        self.hovering = False
        self.globalCounter = 0

        #Jumping variables
        self.jumping = False
        self.jump_counter = 0

        #Object Handler
        self.obh = ObjectHandler() #ObjectHandler object

        #Default colour constants
        self.red = (255, 0, 0)
        self.yellow = (255, 255, 0)
        self.green = (0, 255, 0)
        self.cyan = (0, 255, 255)
        self.blue = (0, 0, 255)
        self.magenta = (255, 0, 255)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

    def on_init(self):
        pygame.init()
        pygame.display.set_caption(self.title)

    def on_event(self, event, paused):
        if event.type == pygame.QUIT:
            self.is_running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            name = self.obh.check_hovering(x, y, True)

            if name != False:
                if paused:
                    if name == "OPTIONS_TITLE": #Return to Title Screen
                        self.new_scene("Title", (200, 200), 60)
                else:
                    #Buttons on the Title Screen
                    if name == 'TITLE_AI':
                        self.new_scene("AI", (1280, 720), 60)
                        self.status = "AI"
                    elif name == 'TITLE_PLAY':
                        self.new_scene("Game", (1280, 720), 60)
                        self.status = "Game"
                    elif name == 'TITLE_OPTIONS':
                        self.status = "Options"
                    elif name == 'QUIT':
                        self.is_running = False

        if event.type == pygame.KEYDOWN:
            if self.status == "Game":
                if event.key == pygame.K_SPACE:
                    self.jumping = True

        if event.type == pygame.KEYUP:
            if self.status == "Game":
                if event.key == pygame.K_SPACE:
                    self.jumping = False

    def on_loop(self, paused):
        "The standard loop method where all object and physics handling is done"

        if self.jumping:
            if self.jump_counter > 0:
                self.jump_counter -= 1
            else:
                jumped = self.obh.handle_jumping(True)
                if jumped:
                    self.jump_counter = 1
        else:
            self.jump_counter = 0

        self.obh.update_objects()
        self.obh.handle_objects()
        self.obh.handle_moving()
        self.obh.generate_ground(self.globalCounter)
        
        self.clock.tick(self.fps_lim)

        game = self.obh.handle_obstacles()

        if game == False:
            self.is_running = False

    def on_render(self):
        "Render any valid objects"
        self.surface.fill(self.black)
        self.obh.render(self.surface)

    def on_quit(self):
        "Exit the game; close the program"
        pygame.quit()

    def on_execute(self, paused:bool=False):
        "The gameloop; run events, run the loop, render objects and check if the program should close."
        if self.is_running:
            if paused == False:
                self.globalCounter += 1
            for event in pygame.event.get():
                self.on_event(event, paused)
            self.on_loop(paused)
            self.on_render()
        else:
            self.on_quit()

    def get_title(self):
        "Return the Window name"
        return self.title

    def get_status(self):
        "Return the Game status"
        return self.status

    def new_scene(self, title, size:tuple, fps_limit:int, custom_status=False):
        """Create a new scene. This edits the existing window by
changing the title, dimensions and FPS limit, and resetting all existing
objects."""
        self.title = title
        self.size = self.width, self.height = size
        self.is_running = True
        self.fps_lim = fps_limit

        if custom_status == False:
            self.status = self.title
        else:
            self.status = custom_status

        self.surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption(self.title)

        self.obh.cleanup()

    def get_obh(self):
        "Return the ObjectHandler object associated with the Game"
        return self.obh

    def get_colours(self):
        "Return some useful default colours"
        return self.red, self.yellow, self.green, self.cyan, self.blue, self.magenta, self.white, self.black
