import pygame
from pygame.locals import *

import numpy as np
import math

class Scene:
    #Source tutorial: http://pygametutorials.wikidot.com/tutorials-basic
    def __init__(self, title, width, height, fps_lim):

        self.title = title
        self.size = self.width, self.height = width, height
        self.is_running = True
        self.fps_lim = fps_lim

        pygame.init()
        self.surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.is_running = True
        self.clock = pygame.time.Clock()

        pygame.display.set_caption(self.title)
        
        self.objects = {} #All of the Objects currently on stage (includes all of the below), assigned with its layer component
        self.buttons = [] #All of the Buttons currently on stage
        self.dynamic = [] #An array of Objects affected by Physics

        self.layers = {} #A dictionary of arrays in the format: {Layer Number: [objects in layer]}

        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        self.hovering = False

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.is_running = False
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                if button.mouse_is_hovering():
                    if np.all(button.get_colour() >= button.get_default_colour()/2):
                        button.set_colour(button.get_colour()-button.get_default_colour()/10)
                elif np.any(button.get_colour() < button.get_default_colour()):
                    button.set_colour(button.get_colour()+button.get_default_colour()/10)

        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.mouse_is_hovering():
                    pass

    def on_loop(self):
        self.update_objects()
        self.order_objects()

        self.clock.tick(self.fps_lim)
        print(self.clock.get_time())
    
    def on_render(self):

        self.surface.fill(self.black)

        for layer in self.layers:
            for object in self.layers[layer]:
                pygame.draw.rect(self.surface, object.get_colour(), object.get_rect())

        for button in self.buttons:
            t = button.get_textobj()
            text = t.font.render(t.text, t.antialias, t.colour, t.bg)
            self.surface.blit(text, button.get_rect())

        pygame.display.update()

    def on_quit(self):
        pygame.quit()

    def on_execute(self):
        if self.__init__ == False:
            self.is_running = False

        while self.is_running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_quit()

    def set_title(self, new_title):
        self.title = new_title

    def get_title(self):
        return self.title

    def add_object(self, object):
        self.objects.update({object: object.get_layer()})

    def remove_object(self, object):
        self.objects.remove(object)

    def update_objects(self):
        for button in self.buttons:
            if button in self.objects:
                pass
            else:
                self.buttons.remove(button) #If a Button is not in Objects, then it will not be used so it can be silently discarded.

        for dynamic_object in self.dynamic:
            if dynamic_object in self.objects:
                pass
            else:
                self.dynamic.remove(dynamic_object) #If a Dynamic Object is not an active Object, there is no reason to keep it.

    def order_objects(self):
        for object in self.objects:

            layer = self.objects[object]

            if layer not in self.layers: #If the layer doesn't exist...
                self.layers.update({layer: [object]}) #...create a new entry in the dictionary for that layer
            else:
                objects_in_layer = self.layers[layer]
                objects_in_layer.append(object)
                self.layers.update({layer: objects_in_layer}) #Add the object to the objects_in_layer and update the dictionary

    def get_objects(self):
        return self.objects

    def add_button(self, buttons):
        if isinstance(buttons, list):
            for button in buttons:
                if isinstance(button, UI):
                    self.buttons.append(button)
                else:
                    raise TypeError("Invalid type: A button must be a UI-type object.")
        else:
            if isinstance(buttons, UI):
                self.buttons.append(buttons)
            else:
                raise TypeError("Invalid type: A button must be a UI-type object.")

    def remove_button(self, buttons):
        self.buttons.remove(buttons)

    def get_buttons(self):
        return self.buttons

    def add_dynamic(self, objects):
        self.dynamic.append(objects)

    def remove_dynamic(self, objects):
        self.dynamic.remove(objects)

    def clear_dynamic(self):
        self.dynamic = []

    def get_dynamic(self):
        return self.dynamic

class TextObject:
    def __init__(self, text, font:pygame.font.Font, colour:pygame.Color, antialias=True, background=None):
        self.text = text
        self.font = font
        self.colour = np.array(colour)
        self.default_colour = np.array(colour)
        self.antialias = antialias
        self.bg = background

class Object:
    def __init__(self, id, rect:pygame.Rect, colour:pygame.Color, layer:int, width:int=0, image=None):
        self.id = id #A unique decimal identifier which shows which object type it is
        self.rect = pygame.Rect(rect) #Attempt to convert the rect to pygame.Rect type
        self.colour = np.array(colour) #A 24-bit tuple to display colour
        self.default_colour = np.array(colour) #This is constant - there is no set_default_colour() method.
        self.layer = layer
        self.width = width
        self.image = image

    def set_id(self, id:int):
        self.id = id

    def get_id(self):
        return self.id

    def set_rect(self, rect:pygame.Rect):
        self.rect = rect

    def get_rect(self):
        return self.rect

    def set_colour(self, colour:pygame.Color):
        self.colour = colour

    def get_colour(self):
        return self.colour

    def get_default_colour(self):
        return self.default_colour

    def set_layer(self, layer:int):
        self.layer = layer
        
    def get_layer(self):
        return self.layer

    def move(self, dir, distance:float):
        if dir == 'x':
            newrect = pygame.Rect(self.rect).move(distance, 0)
        elif dir == 'y':
            newrect = pygame.Rect(self.rect).move(0, distance)
            
        self.set_rect(newrect)

    def set_centre(self, x:int, y:int):
        self.rect.center = (x, y)

    def set_centre_to_centre_of_surface(self, axis=None):
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

    def apply_vec(self, vec:pygame.math.Vector2):
        newrect = self.rect.move(vec)

        self.set_rect(newrect)

    def apply_force(self, magnitude:float, direction:float, unit_is_degrees:bool=False):
        if unit_is_degrees:
            x = magnitude * math.cos(math.radians(direction)) #Conversion of degrees to radians, as python handles sin in radians.
            y = magnitude * math.sin(math.radians(direction)) #Degrees -> Radians: Divide by 180, multiply by pi
        else:
            x = magnitude * math.cos(direction)
            y = magnitude * math.sin(direction)

        newrect = self.rect.move(x, y)
        self.set_rect(newrect)

class UI(Object): #A normal object, with a TextObject assigned to it to allow it to be a functioning UI element.
    def __init__(self, id, rect:pygame.Rect, colour:pygame.Color, layer:int, width:int=0, image=None, textobj:TextObject=None):
        super().__init__(id, rect, colour, layer, width, image)

        self.textobj = textobj

    def set_textobj(self, textobj):
        self.textobj = textobj

    def get_textobj(self):
        return self.textobj

    def mouse_is_hovering(self):
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]

        if x in range(self.rect.left + 1, self.rect.left + self.rect.width):
            if y in range(self.rect.top + 1, self.rect.top + self.rect.height):
                return True

        return False

class Obstacle(Object):
    def __init__(self, id, rect:pygame.Rect, colour:pygame.Color, layer:int, width=0, image=None):
        super().__init__(id, rect, colour, layer, width, image)
