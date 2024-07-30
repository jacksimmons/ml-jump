import pygame
import numpy as np
import math
import random


class Object:
    def __init__(self, rect: pygame.Rect, colour: pygame.Color, width:int=5, image=None):
        self.rect: pygame.Rect = pygame.Rect(rect)
        self.colour = np.array(colour)
        self.default_colour = np.array(colour)
        self.width = width
        self.image = image

        self.h_velocity = 0 #Horizontal velocity
        self.v_velocity = 0 #Vertical velocity

    def set_rect(self, rect: pygame.Rect):
        "Set the rectangular position of the object"
        self.rect = rect

    def get_rect(self):
        "Get the rectangular position of the object"
        return self.rect

    def get_left(self):
        "Get the x ('left') component of the object's rect"
        return self.rect.x

    def get_top(self):
        "Get the y ('top') component of the object's rect"
        return self.rect.y

    def get_w(self):
        "Get the w ('width') component of the object's rect"
        return self.rect.w

    def get_h(self):
        "Get the h ('height') component of the object's rect"
        return self.rect.h

    def set_axis_centre(self, axis, pos:int):
        "Sets the object's x or y centre"
        if axis == "x":
            self.rect.centerx = pos
        elif axis == "y":
            self.rect.centery = pos

    def set_centre(self, x:int, y:int):
        "Set the object's rect's centre"
        self.rect.center = (x, y)

    def set_axis_to_centre(self, axis=None):
        "Set the object's rect's x or y component's centre"
        surface = pygame.display.get_surface()
        if surface is not None:
            if axis == 'x':
                self.rect.centerx = surface.get_width()/2
            elif axis == 'y':
                self.rect.centery = surface.get_height()/2
            elif axis is None:
                self.rect.center = (surface.get_width()/2, surface.get_height()/2)
            else:
                print("Invalid axis entered.")
        else:
            print("No surface found.")

    def set_colour(self, colour:pygame.Color):
        "Set the colour of the rect"
        self.colour = colour

    def get_colour(self):
        "Get the colour of the rect"
        return self.colour

    def get_default_colour(self):
        "Get the default colour of the rect (i.e. the colour it was created with)"
        return self.default_colour

    def colour_is_default(self):
        "Check if the rect's colour is equal to its default_colour"
        return np.all(self.colour == self.default_colour)

    def move(self, velocity):
        "Move the object by a tuple of x and y velocity"
        if isinstance(velocity, tuple):
            h_velocity = velocity[0]
            v_velocity = velocity[1]
            self.rect = self.rect.move(h_velocity, v_velocity)

    def set_component_velocity(self, component, velocity):
        "Set the x/y velocity of the object"
        if component == 'x':
            self.h_velocity = velocity
        elif component == 'y':
            self.v_velocity = velocity

    def get_component_velocity(self, component):
        "Get the x/y velocity of the object"
        if component == 'x':
            return self.h_velocity
        elif component == 'y':
            return self.v_velocity

    def set_velocity(self, velocity):
        "Set the velocity of the object with a tuple"
        if isinstance(velocity, tuple):
            self.h_velocity, self.v_velocity = velocity
        else:
            print("Not a tuple. Use set_component_velocity()")

    def get_velocity(self):
        "Get both the x and y velocities of the object"
        return (self.h_velocity, self.v_velocity)

    def accelerate(self, direction, acceleration):
        "Increase the x/y velocity by an integer amount"
        if direction == 'x':
            self.h_velocity += acceleration
        elif direction == 'y':
            self.v_velocity += acceleration


class TextObject:
    def __init__(self, text, font:pygame.font.Font, colour:pygame.Color, antialias=True, background=None):
        self.text = text
        self.font = font
        self.colour = np.array(colour)
        self.default_colour = np.array(colour)
        self.antialias = antialias
        self.bg = background

    def set_text(self, newtext):
        "Set the assigned text"
        self.text = newtext

    def get_text(self):
        "Get the assigned text"
        return self.text

    def set_colour(self, colour):
        "Set the colour of the assigned text"
        self.colour = colour

    def get_colour(self, colour):
        "Get the colour of the assigned text"
        return self.colour


class UI(Object): #A normal object, with a TextObject assigned to it to allow it to be a functioning UI element.
    def __init__(self, rect:pygame.Rect, colour:pygame.Color, name=None, textobj:TextObject=None, width:int=0, image=None):
        super().__init__(rect, colour, width, image)

        self.textobj = textobj
        self.name = name
        self.mouse_is_hovering = False

    def set_textobj(self, textobj):
        "Set the TextObject"
        self.textobj = textobj

    def get_textobj(self):
        "Get the TextObject"
        return self.textobj

    def get_name(self):
        "Get the name - differentiates the UI object from others"
        return self.name

    def set_hovering(self, mouse_is_hovering:bool):
        "Set the mouse_is_hovering attribute"
        self.mouse_is_hovering = mouse_is_hovering

    def get_hovering(self):
        "Get the mouse_is_hovering attribute"
        return self.mouse_is_hovering

    def fade(self, degree:int, minimum_ratio:int=0.3):
        "Fade a UI object's colour (useful for when the mouse is hovering over a button)"
        skip = False

        if np.any((self.colour - self.default_colour / degree) < self.default_colour * minimum_ratio):
            skip = True
        elif np.any(self.colour < self.default_colour * minimum_ratio):
            skip = True

        if skip:
            self.colour = self.default_colour * minimum_ratio
        else:
            self.colour = self.colour - self.default_colour / degree

    def unfade(self, degree:int, maximum_ratio:int=1):
        "Unfade a UI object's colour - the reverse of fade."
        skip = False

        if np.any((self.colour + self.default_colour / degree) > self.default_colour * maximum_ratio):
            skip = True
        elif np.any(self.colour > self.default_colour * maximum_ratio):
            skip = True

        if skip:
            self.colour = self.default_colour * maximum_ratio
        else:
            self.colour = self.colour + self.default_colour / degree