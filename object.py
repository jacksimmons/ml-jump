import pygame

import numpy as np
import math

class ObjectHandler:
    def __init__(self):
        #Object lists used to group object types together
        self.objects = [] #All of the Objects currently on stage (should include all of the below)
        self.ui = [] #All of the Buttons currently on stage (must inherit from UI)
        self.ground = [] #An array of Objects that act as valid ground for dynamic objects to move along

        #Obstacles and moving objects
        self.moving = [] #An array of Objects that are scrolling from the right side of the screen to the left.
        self.obstacles = [] #An array of Objects that kill the player on contact.
        self.object_speed = 5 #The speed at which the moving objects move (pixels per frame)

        #Player variables
        self.player = None #The current Player object
        self.player_grounded = False
        self.player_g_cnt = 0

    #---------------------------------------------------------------------------------
    #Standard Object-Handling methods
    #---------------------------------------------------------------------------------

    def cleanup(self): #For effectively creating a new canvas
        self.__init__()

    def handle_objects(self):

        x, y = pygame.mouse.get_pos()
        for ui in self.ui:
            if ui.get_hovering():
                if ui.get_rect().collidepoint(x, y):
                    ui.fade(20)
                else:
                    ui.set_hovering(False)
            else:
                if ui.get_rect().collidepoint(x, y):
                    ui.set_hovering(True)
                elif ui.colour_is_default() == False:
                    ui.unfade(20)

        if self.player is not None:
            if self.player_grounded:
                #ground_y = self.locate_active_ground()
                if self.player.get_component_velocity('y') > 0:
                    self.player.set_component_velocity('y', 0)
                self.player_g_cnt = 0

            else:
                if self.player_g_cnt == 5:
                    self.player.accelerate('y', 2)
                    self.player_g_cnt = 0

                self.player_g_cnt += 1

            p = self.player.get_rect()
            if p.y <= self.ground[0].get_rect().y:
                #If the player's y position is less than the object's y position (i.e. above it):

                self.player_grounded = False
                #If none of the ground objects are touching the player, this default value of player_grounded will be used.
                for g in self.ground:

                    r = g.get_rect()

                    #if p.collidepoint(r.centerx, p.y): #Check if they are on roughly the same x position
                    if p.colliderect(r.x, r.y-1, r.w, r.h):
                        self.player_grounded = True

                    if p.colliderect(r):
                        self.player.set_component_velocity('y', 0)
                        self.upwarp(p, r)
                        self.player_grounded = True
                
                    if r.colliderect(p.x, p.y + self.player.get_component_velocity('y'), p.w, p.h):
                        #If the object will go through the ground on the next frame, it must stop immediately.
                        #This works both for going downwards through a floor and upwards through a floor (ceiling).
                        self.player.set_component_velocity('y', 0)
                        self.downwarp(p, r)

        for object in self.objects:

            object.move(object.get_velocity())

            r = object.get_rect()
            sx, sy = pygame.display.get_surface().get_size()
            
            if object is not self.player:
                if r.x + r.w < 0:
                    self.objects.remove(object)
                    del object

                if r.y + r.h < 0:
                    self.objects.remove(object)
                    del object

                if r.w < 0 or r.h < 0: #Illegal object (negative length sides)
                    self.objects.remove(object)
                    del object

    def add_object(self, object):
        self.objects.append(object)

    def remove_object(self, object):
        self.objects.remove(object)

    def update_objects(self):
        for ui in self.ui:
            if ui not in self.objects:
                self.ui.remove(ui) #If an object is not in Objects, then it will not be used so it can be silently discarded.

        for g in self.ground:
            if g not in self.objects:
                self.ground.remove(g)

        for m in self.moving:
            if m not in self.objects:
                self.moving.remove(m)

        for o in self.obstacles:
            if o not in self.objects:
                self.obstacles.remove(o)

    def get_objects(self):
        return self.objects

    #Button Objects
    def check_hovering(self, x, y, return_name:bool=False, update_button:bool=False):
        if self.ui != []:
            for ui in self.ui:
                if update_button:
                    ui.set_hovering(ui.get_rect().collidepoint(x,y))

                if return_name:
                    return ui.get_rect().collidepoint(x,y), ui.get_name()
                else:
                    return ui.get_rect().collidepoint(x,y)
        else:
            return None, None

    def add_ui(self, ui):
        self.ui.append(ui)

    def remove_ui(self, ui):
        self.ui.remove(ui)

    def get_ui(self):
        return self.ui

    #Objects that act as Ground
    def add_ground(self, object):
        self.ground.append(object)

    def remove_ground(self, object):
        self.ground.remove(object)

    #Player Objects
    def set_player(self, player):
        self.player = player

    def handle_jumping(self, jump:bool):
        if jump:
            if self.player_grounded == True:
                p = self.player.get_rect()

                self.player.set_rect(pygame.Rect(p.x, p.y-1, p.w, p.h))
                #Move the player 1 pixel up so the program doesn't think they are still on the ground
                self.player.accelerate('y', -8)
                return True
            return False

    def upwarp(self, p:pygame.Rect, g:pygame.Rect):
        while p.y > g.y - p.h:
            p.y -= 1
        self.player.set_rect(p)

    def downwarp(self, p:pygame.Rect, g:pygame.Rect):
        while p.y + p.h < g.y:
            p.y += 1
        self.player.set_rect(p)

    #Moving objects
    def add_obstacle(self, obstacle):
        self.obstacles.append(obstacle)

    def remove_obstacle(self, obstacle):
        self.obstacles.remove(obstacle)

    def add_moving(self, moving):
        self.moving.append(moving)

    def remove_moving(self, moving):
        self.moving.remove(moving)

    def handle_obstacles(self):
        for o in self.obstacles:
            if o.get_rect().colliderect(self.player.get_rect()):
                return False
            return True

    def handle_moving(self):
        for m in self.moving:
            m.set_component_velocity('x', -self.object_speed)

    #---------------------------------------------------------------------------------
    #Rendering
    #---------------------------------------------------------------------------------

    def render(self, surface):
        for object in self.objects:
            pygame.draw.rect(surface, object.get_colour(), object.get_rect())

        for u in self.ui:
            t = u.get_textobj()
            text = t.font.render(t.text, t.antialias, t.colour, t.bg)
            surface.blit(text, u.get_rect())

        pygame.display.update()

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
