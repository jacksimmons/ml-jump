import pygame

import numpy as np
import math

class TextObject:
    def __init__(self, text, font:pygame.font.Font, colour:pygame.Color, antialias=True, background=None):
        self.text = text
        self.font = font
        self.colour = np.array(colour)
        self.default_colour = np.array(colour)
        self.antialias = antialias
        self.bg = background

class Object:
    def __init__(self, rect:pygame.Rect, colour:pygame.Color, width:int=0, image=None):
        self.rect = pygame.Rect(rect) #Attempt to convert the rect to pygame.Rect type
        self.colour = np.array(colour) #A 24-bit tuple to display colour
        self.default_colour = np.array(colour) #This is constant - there is no set_default_colour() method.
        self.width = width
        self.image = image

#       self.is_grounded = False

        self.h_velocity = 0 #Horizontal velocity
        self.v_velocity = 0 #Vertical velocity

    def set_rect(self, rect:pygame.Rect):
        self.rect = rect

    def get_rect(self):
        return self.rect

    def set_centre(self, x:int, y:int):
        self.rect.center = (x, y)

    def set_axis_to_centre(self, axis=None):
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
        self.colour = colour

    def get_colour(self):
        return self.colour

    def get_default_colour(self):
        return self.default_colour

    def colour_is_default(self):
        return np.all(self.colour == self.default_colour)

    def move(self, velocity):
        if isinstance(velocity, tuple):
            h_velocity = velocity[0]
            v_velocity = velocity[1]
            self.rect = self.rect.move(h_velocity, v_velocity)

    def set_component_velocity(self, component, velocity):
        if component == 'x':
            self.h_velocity = velocity
        elif component == 'y':
            self.v_velocity = velocity

    def get_component_velocity(self, component):
        if component == 'x':
            return self.h_velocity
        elif component == 'y':
            return self.v_velocity

    def set_velocity(self, velocity):
        if isinstance(velocity, tuple):
            self.h_velocity, self.v_velocity = velocity
        else:
            print("Not a tuple. Use set_component_velocity()")

    def get_velocity(self):
        return (self.h_velocity, self.v_velocity)

    def accelerate(self, direction, acceleration):
        if direction == 'x':
            self.h_velocity += acceleration
        elif direction == 'y':
            self.v_velocity += acceleration

#    def set_grounded(self, is_grounded:bool):
#        self.is_grounded = is_grounded

#    def get_grounded(self):
#        return self.is_grounded

    def set_mass(self, mass:int):
        self.mass = mass

    def get_weight(self):
        return self.mass * 9.81

    def apply_force(self, magnitude:float, bearing:int, unit_is_degrees:bool=False):

        magnitude = round(magnitude)

        if unit_is_degrees and 0 <= bearing < 360:
            x = magnitude * math.cos(math.radians(bearing)) #Conversion of degrees to radians, as python handles sin in radians.
            y = magnitude * math.sin(math.radians(bearing)) #Degrees -> Radians: Divide by 180, multiply by pi
        elif 0 <= bearing < math.pi:
            x = magnitude * math.cos(bearing)
            y = magnitude * math.sin(bearing)

        self.rect = self.rect.move(x, y)

class Player(Object): #A player version of the standard Object class.
    def __init__(self, rect:pygame.Rect, colour:pygame.Color, width:int=0, image=None):
        super().__init__(rect, colour, width, image)

        self.status = True #Boolean status to indicate whether the Player is alive (True) or dead (False)

    def get_status(self):
        return self.status

    def set_status(self, status:bool):
        self.status = status

class UI(Object): #A normal object, with a TextObject assigned to it to allow it to be a functioning UI element.
    def __init__(self, rect:pygame.Rect, colour:pygame.Color, name=None, textobj:TextObject=None, width:int=0, image=None):
        super().__init__(rect, colour, width, image)

        self.textobj = textobj
        self.name = name
        self.mouse_is_hovering = False

    def set_textobj(self, textobj):
        self.textobj = textobj

    def get_textobj(self):
        return self.textobj

    def get_name(self):
        return self.name

    def set_hovering(self, mouse_is_hovering:bool):
        self.mouse_is_hovering = mouse_is_hovering

    def get_hovering(self):
        return self.mouse_is_hovering

    def fade(self, degree:int, minimum_ratio:int=0.3):
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
        skip = False

        if np.any((self.colour + self.default_colour / degree) > self.default_colour * maximum_ratio):
            skip = True
        elif np.any(self.colour > self.default_colour * maximum_ratio):
            skip = True

        if skip:
            self.colour = self.default_colour * maximum_ratio
        else:
            self.colour = self.colour + self.default_colour / degree

class Obstacle(Object):
    def __init__(self, rect:pygame.Rect, colour:pygame.Color, width=0, image=None):
        super().__init__(rect, colour, width, image)
