import pygame
from pygame.locals import *

from object import *
#TextObject, Object, Player, UI, Obstacle

import numpy as np
import math
import sys

class Game:
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
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
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
                    if name == 'TITLE_PLAY':
                        self.new_scene("Game", (640, 480), 60)
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
        """The standard loop method where all object and physics
handling is ordered"""

        if self.jumping:
            if self.jump_counter > 0:
                self.jump_counter -= 1
            else:
                jumped = self.obh.handle_jumping(True)
                if jumped:
                    self.jump_counter = 1

        else:
            self.jump_counter = 0

        tenth_frame = False
        if self.globalCounter % (self.fps_lim/10) == 0:
            tenth_frame = True

        self.obh.update_objects()
        self.obh.handle_objects()

        game = self.obh.handle_obstacles()

        if game == False:
            self.is_running = False

        self.obh.create_obstacle(self.globalCounter)

        self.obh.handle_moving()

        self.clock.tick(self.fps_lim)

    def on_render(self):
        """Render any objects currently in the Scene"""
        self.surface.fill(self.black)
        self.obh.render(self.surface)

    def on_quit(self):
        """Exit the game; close the program"""
        pygame.quit()
        #sys.exit()

    def on_execute(self, paused:bool=False):
        """The gameloop; run events, run the loop, render objects,
and check if the program should close."""
        if self.is_running:
            if paused == False:
                self.globalCounter += 1
            for event in pygame.event.get():
                self.on_event(event, paused)
            self.on_loop(paused)
            self.on_render()
        else:
            self.on_quit()

    def set_title(self, new_title):
        self.title = new_title

    def get_title(self):
        return self.title

    def get_status(self):
        return self.status

    def new_scene(self, title, size:tuple, fps_limit:int, custom_status=False):
        """Create a new scene. This can edit the existing window by
changing the title, dimensions and FPS limit, and resets all existing
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

    #def locate_active_ground(self):
#        x, y, w, h = self.player.get_rect()
#        temp = Object((x, y, 1, 1), self.green)
#        for g in self.ground:
#            if temp.get_rect().colliderect(g.get_rect()):
#                break
#        print(temp.get_rect())
#        if self.player_in_ground:
#            temp.move((0,1))
#        else:
#            temp.move((0,-1))
#        return temp.get_rect().y

    def get_obh(self):
        return self.obh

    def get_colours(self):
        return self.red, self.green, self.blue, self.white, self.black