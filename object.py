import pygame

import numpy as np
import math

import random
from obstacle_generator import ObjectGenerator

class ObjectHandler:
    def __init__(self):
        #Object lists used to group object types together
        self.objects = [] #All of the Objects currently on stage (should include all of the below)
        self.ground = [] #An array of Objects that act as valid ground for dynamic objects to move along
        self.floor = None

        #Obstacles and physics
        self.moving = [] #An array of Objects that are scrolling from the right side of the screen to the left.
        self.obstacles = [] #An array of Objects that kill the player on contact.
        self.object_speed = 5 #The speed at which the moving objects move left (pixels per frame)
        self.jump_strength = 8 #How powerful the player's jump is
        self.g_strength = -3 #The acceleration due to gravity that the player receives (i.e. gravitational strength)

        self.obg = ObjectGenerator(self) #The ObjectGenerator

        #UI elements
        self.ui = [] #All of the Buttons currently on stage (must inherit from UI)
        self.display_pos = None
        self.display_grounded = None
        self.display_floored_cnt = None
        self.score = None

        #Player variables
        self.player = None #The current Player object
        self.player_grounded = False
        self.player_floored = False
        self.player_floored_cnt = 0
        self.player_g_cnt = 0

        #Colours
        self.white = (255, 255, 255)

    #---------------------------------------------------------------------------------
    #Standard Object-Handling methods
    #---------------------------------------------------------------------------------

    def cleanup(self): #For effectively creating a new canvas
        self.__init__()

    def handle_objects(self):

        x, y = pygame.mouse.get_pos()
        for ui in self.ui:

            if self.score is not None:
                cur_score = int(self.score.get_textobj().get_text()[7:])
                self.score.get_textobj().set_text("Score: " + str(cur_score + 1))

            if self.display_pos is not None and self.player is not None:
                self.display_pos.get_textobj().set_text("Player Rect: " + str(self.player.get_rect()))

            if self.display_grounded is not None:
                t = self.display_grounded.get_textobj()
                status = "Airbourne"
                colour = (255, 0, 255)
                if self.player_floored:
                    colour = (0, 255, 0)
                    status = "Floored"
                elif self.player_grounded:
                    colour = (0, 0, 255)
                    status = "Grounded"
                t.set_colour(colour)
                t.set_text("Player Ground Status: " + status)

            if self.display_floored_cnt is not None:
                self.display_floored_cnt.get_textobj().set_text("Floored Timer: " + str(self.player_floored_cnt))

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
                    self.player.accelerate('y', -self.g_strength)
                    self.player_g_cnt = 0

                self.player_g_cnt += 1

            p = self.player.get_rect()

            if p.y + p.h < self.get_floor().get_y():
                #If the player's y position is less than the floor's y position (i.e. above it):

                self.player_grounded = False
                self.player_floored = False
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

            elif p.y + p.h == self.get_floor().get_y():
                self.player_grounded = True
                self.player_floored = True
                self.player_floored_cnt += 1

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
        "Validate an object"
        self.objects.append(object)

    def remove_object(self, object):
        "Invalidate an object"
        self.objects.remove(object)

    def update_objects(self):
        "Check objects for validity."
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
        "Return valid objects"
        return self.objects

    def create_object(self, rect, colour, width:int=0, image=None):
        "Tool for generating an Object"
        return Object(rect, colour, width, image)

    #Button Objects
    def check_hovering(self, x, y, return_name:bool=False, update_button:bool=False):
        "Check if the cursor is hovering over a UI element."
        if self.ui != []:
            for ui in self.ui:
                if update_button:
                    ui.set_hovering(ui.get_rect().collidepoint(x,y))

                if return_name:
                    if ui.get_rect().collidepoint(x,y):
                        return ui.get_name()
                else:
                    if ui.get_rect().collidepoint(x,y):
                        return True
        else:
            return False

    def add_ui(self, ui):
        "Validate a UI element"
        self.ui.append(ui)

    def remove_ui(self, ui):
        "Invalidate a UI element"
        self.ui.remove(ui)

    def get_ui(self):
        "Return all valid UI elements"
        return self.ui

    #Debugging

    def set_score_counter(self, score_counter):
        "Set the UI object that will increment every time the player's score increases"
        self.score = score_counter

    def set_player_pos_disp(self, player_pos):
        "Set the UI object that will display the player's position"
        self.display_pos = player_pos

    def set_player_grounded_disp(self, player_grounded):
        "Set the UI object that will display whether the player is airbourne, grounded or floored."
        self.display_grounded = player_grounded

    def set_player_floored_cnt_disp(self, pfc):
        "Set the UI object that will display the player_floored_cnt attribute"
        self.display_floored_cnt = pfc

    #Objects that act as Ground
    def add_ground(self, object):
        "Validate a Ground object"
        self.ground.append(object)

    def remove_ground(self, object):
        "Invalidate a Ground object"
        self.ground.remove(object)

    #Player Objects
    def set_player(self, player):
        "Set the player object"
        self.player = player

    def get_player(self):
        "Return the player object"
        return self.player

    def handle_jumping(self, jump:bool):
        "Check whether the player has jumped, and executes the jump if so"
        if jump:
            if self.player_grounded == True:
                p = self.player.get_rect()

                self.player.set_rect(pygame.Rect(p.x, p.y-1, p.w, p.h))
                #Move the player 1 pixel up so the program doesn't think they are still on the ground
                self.player.accelerate('y', -self.jump_strength)
                return True
            return False

    def upwarp(self, p:pygame.Rect, g:pygame.Rect):
        "Moves the player upwards until they are above the provided Ground"
        while p.y > g.y - p.h:
            p.y -= 1
        self.player.set_rect(p)

    def downwarp(self, p:pygame.Rect, g:pygame.Rect):
        "Moves the player downwards until they are below the provided Ground"
        while p.y + p.h < g.y:
            p.y += 1
        self.player.set_rect(p)

    #Moving objects
    def add_obstacle(self, obstacle):
        "Validate an obstacle"
        self.obstacles.append(obstacle)

    def remove_obstacle(self, obstacle):
        "Invalidate an obstacle"
        self.obstacles.remove(obstacle)

    def get_moving_speed(self):
        "Return the default object movement speed"
        return self.object_speed

    def add_moving(self, moving):
        "Validate a moving object"
        self.moving.append(moving)

    def remove_moving(self, moving):
        "Invalidate a moving object"
        self.moving.remove(moving)

    def get_moving(self):
        "Return all valid moving objects"
        return self.moving

    def handle_moving(self):
        "Handle object movement"
        for m in self.moving:
            m.set_component_velocity('x', -self.object_speed)

    def generate_ground(self, timer):
        "Generate ground randomly based on the player's position"
        self.obg.handle_generation(self)

    #Obstacles
    def handle_obstacles(self):
        "Handle obstacle collision with the player"
        o_rects = [o.get_rect() for o in self.obstacles]
        if self.player is not None:
            for r in o_rects:
                if r.colliderect(self.player.get_rect()):
                    return False
            return True

    #Floor Collision
    def get_floor(self):
        "Return the floor if possible, otherwise return the first ground object validated"
        if self.floor is not None:
            return self.floor
        else:
            return self.ground[0] #If no floor can be found, resort to the first rendered ground object.

    def set_floor(self, floor):
        "Set the floor object"
        self.floor = floor

    #---------------------------------------------------------------------------------
    #Rendering
    #---------------------------------------------------------------------------------

    def render(self, surface):
        "Handles all rendering"
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

class Object:
    def __init__(self, rect:pygame.Rect, colour:pygame.Color, width:int=5, image=None):
        self.rect = pygame.Rect(rect) #Attempt to convert the rect to pygame.Rect type
        self.colour = np.array(colour) #A 24-bit tuple to display colour
        self.default_colour = np.array(colour) #This is constant - there is no set_default_colour() method.
        self.width = width
        self.image = image

        self.h_velocity = 0 #Horizontal velocity
        self.v_velocity = 0 #Vertical velocity

    def set_rect(self, rect:pygame.Rect):
        "Set the rectangular position of the object"
        self.rect = rect

    def get_rect(self):
        "Get the rectangular position of the object"
        return self.rect

    def get_x(self):
        "Get the x ('left') component of the object's rect"
        return self.rect.x

    def get_y(self):
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
