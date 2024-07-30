import pygame
from object import Object
from obstacle_generator import ObstacleGenerator


class ObjectHandler:
    def __init__(self):
        #Object lists used to group object types together
        self.objects: list[Object] = [] #All of the Objects currently on stage (should include all of the below)
        self.ground = [] #An array of Objects that act as valid ground for dynamic objects to move along
        self.floor = None

        #Obstacles and physics
        self.__moving = [] #An array of Objects that are scrolling from the right side of the screen to the left.
        self.__obstacles = [] #An array of Objects that kill the player on contact.
        self.__obj_spd: float = 3.5 #The speed at which the moving objects move left (pixels per frame)
        self.__jump_strength: float = 8 #How powerful the player's jump is
        self.__g_strength: float = -4 #The acceleration due to gravity that the player receives (i.e. gravitational strength)

        self.obg = ObstacleGenerator(self) #The ObjectGenerator

        #UI elements
        self.ui = [] #All of the Buttons currently on stage (must inherit from UI)
        self.display_pos = None
        self.display_grounded = None
        self.display_floored_cnt = None
        self.score = None

        #Player variables
        self.player: Object = None #The current Player object
        self.player_grounded = False
        self.player_floored = False
        self.player_floored_cnt = 0
        self.player_g_cnt = 0

        #Colours
        self.white = (255, 255, 255)

    #---------------------------------------------------------------------------------
    # Standard Object-Handling methods
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
                    self.player.accelerate('y', -self.__g_strength)
                    self.player_g_cnt = 0

                self.player_g_cnt += 1

            p: pygame.Rect = self.player.get_rect()

            # If the player is above the floor...
            if p.bottom < self.get_floor().get_top():
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

            elif p.y + p.h == self.get_floor().get_top():
                self.player_grounded = True
                self.player_floored = True
                self.player_floored_cnt += 1

        for object in self.objects:
            object.move(object.get_velocity())
            r = object.get_rect()

            if object is not self.player:
                if r.right < 0 or r.bottom < 0:
                    self.objects.remove(object)

    def add_object(self, object):
        "Validate an object"
        self.objects.append(object)

    def remove_object(self, object):
        "Invalidate an object"
        self.objects.remove(object)
        
        for ui in self.ui:
            if ui not in self.objects:
                self.ui.remove(ui) #If an object is not in Objects, then it will not be used so it can be silently discarded.

        for g in self.ground:
            if g not in self.objects:
                self.ground.remove(g)

        for m in self.__moving:
            if m not in self.objects:
                self.__moving.remove(m)

        for o in self.__obstacles:
            if o not in self.objects:
                self.__obstacles.remove(o)

    def get_objects(self):
        "Return valid objects"
        return self.objects

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
        self.add_object(ui)

    def remove_ui(self, ui):
        "Invalidate a UI element"
        self.ui.remove(ui)
        self.remove_object(ui)

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
        self.add_object(object)

    def remove_ground(self, object):
        "Invalidate a Ground object"
        self.ground.remove(object)
        self.remove_object(object)

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
                self.player.accelerate('y', -self.__jump_strength)
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
        self.__obstacles.append(obstacle)

    def remove_obstacle(self, obstacle):
        "Invalidate an obstacle"
        self.__obstacles.remove(obstacle)

    def get_moving_speed(self):
        "Return the default object movement speed"
        return self.__obj_spd

    def add_moving(self, moving: Object):
        "Validate a moving object"
        moving.set_component_velocity('x', -self.__obj_spd)
        self.__moving.append(moving)

    def remove_moving(self, moving):
        "Invalidate a moving object"
        self.__moving.remove(moving)

    def get_moving(self):
        "Return all valid moving objects"
        return self.__moving

    def generate_ground(self, timer):
        "Generate ground randomly based on the player's position"
        self.obg.handle_generation(self)

    #Obstacles
    def handle_obstacles(self) -> bool:
        "Handle death collision with the player"
        o_rects = [o.get_rect() for o in self.__obstacles]
        if self.player is not None:
            for r in o_rects:
                if r.colliderect(self.player.get_rect()):
                    print("Hi")
                    return False
        return True

    #Floor Collision
    def get_floor(self) -> Object:
        "Returns the floor if possible, otherwise return the first ground object validated"
        if self.floor is not None:
            return self.floor
        else:
            return self.ground[0] #If no floor can be found, resort to the first rendered ground object.

    def set_floor(self, floor: Object):
        "Set the floor object"
        self.floor = floor

    #---------------------------------------------------------------------------------
    #Rendering
    #---------------------------------------------------------------------------------

    def render(self, surface: pygame.surface):
        "Handles all rendering"
        for object in self.objects:
            pygame.draw.rect(surface, object.get_colour(), object.get_rect())
            pygame.draw.rect(surface, (255, 0, 0), object.get_rect(), 2)

        for u in self.ui:
            t = u.get_textobj()
            text = t.font.render(t.text, t.antialias, t.colour, t.bg)
            surface.blit(text, u.get_rect())

        pygame.display.update()