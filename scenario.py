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

        #Misc variables
        self.player = None #The current Player object
        self.player_in_ground = False

        #Object lists used to group object types together
        self.objects = [] #All of the Objects currently on stage (should include all of the below)
        self.buttons = [] #All of the Buttons currently on stage (must inherit from UI)
        self.dynamic = [] #An array of Objects affected by Physics
        self.ground = [] #An array of Objects that act as valid ground for dynamic objects to move along

        #Default colour constants
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

    def on_init(self):
        pygame.init()
        pygame.display.set_caption(self.title)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.is_running = False

        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            for button in self.buttons:
                if button.get_rect().collidepoint(x,y):
                    button.set_hovering(True)
                else:
                    button.set_hovering(False)

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for button in self.buttons:
                if button.get_rect().collidepoint(x,y):
                    if button.get_name() == "TITLE_PLAY":
                        self.new_scene("Game", (640, 480), 60)
                        self.status = "Game"


        if event.type == pygame.KEYDOWN:
            if self.status == "Game":
                #if event.key == pygame.K_d:
                #    self.player.set_component_velocity('x', 5)
                #if event.key == pygame.K_a:
                #    self.player.set_component_velocity('x', -5)
                if event.key == pygame.K_SPACE and self.player.get_jumping() == False:
                    self.player.set_component_velocity('y', -5)
                    self.player.set_jumping(True)
                #if event.key == pygame.K_s:
                #    self.player.set_component_velocity('y', 5)

        if event.type == pygame.KEYUP:
            if self.status == "Game":
                #if event.key == pygame.K_d:
                #    self.player.set_component_velocity('x', 0)
                #if event.key == pygame.K_a:
                #    self.player.set_component_velocity('x', 0)
                if event.key == pygame.K_SPACE and self.player.get_jumping():
                    self.player.set_component_velocity('y', 0)
                #if event.key == pygame.K_s:
                #    self.player.set_component_velocity('y', 0)

    def on_loop(self):
        tenth_frame = False
        if self.globalCounter % (self.fps_lim/10) == 0:
            tenth_frame = True

        self.update_objects()

        x, y = pygame.mouse.get_pos()
        for button in self.buttons:
            if button.get_hovering():
                if button.get_rect().collidepoint(x, y):
                    button.fade(20)
                else:
                    button.set_hovering(False)
            else:
                if button.get_rect().collidepoint(x, y):
                    button.set_hovering(True)
                elif button.colour_is_default() == False:
                    button.unfade(20)

        if self.status == "Game" and self.player is not None:
            if self.player_in_ground:
                #ground_y = self.locate_active_ground()
                if self.player.get_component_velocity('y') > 0:
                    self.player.set_component_velocity('y', 0)

            elif tenth_frame:
                #This ensures it only happens 10 times per second by checking the framerate with the globalCounter
                self.player.accelerate('y', 1)

            for g in self.ground:
                r = g.get_rect()
                p = self.player.get_rect()
                
                rx, ry, rw, rh = r.x, r.y, r.w, r.h
                buffer = pygame.Rect(rx, ry-1, rw, rh)
                
                if p.colliderect(buffer):
                    self.player.set_jumping(False)
                
                if p.colliderect(r):
                    self.player_in_ground = True
                elif pygame.Rect((p.x, p.y + self.player.get_component_velocity('y'), p.w, p.h)).colliderect(r):
                    self.player.set_component_velocity('y', 0)
                else:
                    self.player_in_ground = False

        for object in self.objects:
            object.move(object.get_velocity())

        self.clock.tick(self.fps_lim)

    def on_render(self):
        self.surface.fill(self.black)

        for object in self.objects:
            pygame.draw.rect(self.surface, object.get_colour(), object.get_rect())

        for button in self.buttons:
            t = button.get_textobj()
            text = t.font.render(t.text, t.antialias, t.colour, t.bg)
            self.surface.blit(text, button.get_rect())

        pygame.display.update()

    def on_quit(self):
        pygame.quit()
        sys.exit()

    def on_execute(self):
        if self.is_running:
            self.globalCounter += 1
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        else:
            self.on_quit()

    def set_title(self, new_title):
        self.title = new_title

    def get_title(self):
        return self.title

    def get_status(self):
        return self.status

    def new_scene(self, title, size:tuple, fps_limit:int):
        self.title = title
        self.size = self.width, self.height = size
        self.is_running = True
        self.fps_lim = fps_limit

        self.surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption(self.title)

        self.objects = []
        self.buttons = []
        self.dynamic = []
        self.ground = []


    def add_object(self, object):
        self.objects.append(object)

    def remove_object(self, object):
        self.objects.remove(object)

    def update_objects(self):
        for button in self.buttons:
            if button not in self.objects:
                self.buttons.remove(button) #If a Button is not in Objects, then it will not be used so it can be silently discarded.

        for dynamic_object in self.dynamic:
            if dynamic_object not in self.objects:
                self.dynamic.remove(dynamic_object) #If a Dynamic Object is not an active Object, there is no reason to keep it.

    def get_objects(self):
        return self.objects

    def add_button(self, button):
        self.buttons.append(button)

    def remove_button(self, button):
        self.buttons.remove(button)

    def get_buttons(self):
        return self.buttons

    def add_dynamic(self, object):
        self.dynamic.append(object)

    def remove_dynamic(self, object):
        self.dynamic.remove(object)

    def get_dynamic(self):
        return self.dynamic

    def add_ground(self, object):
        self.ground.append(object)

    def remove_ground(self, object):
        self.ground.remove(object)

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

    def set_player(self, player):
        self.player = player

    def get_colours(self):
        return self.red, self.green, self.blue, self.white, self.black
