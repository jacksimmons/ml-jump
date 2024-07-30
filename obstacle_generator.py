import random
import statistics
import pygame
import numpy as np
import json
from colour import Colour
from object import Object
from obstacle_formation import ObstacleMatrix, ObstacleRow


class ObstacleGenerator:
    def __init__(self, obh):
        self.obh = obh #The ObjectHandler that instantiated this object
        self.gen_objs: list[Object] = [] #All of the generated objects currently on screen
        self.last_obj_type = None #The type of obstacle/ground last generated
        self.__last_formation: ObstacleMatrix = None

        #Max player jump height = 109 pixels
        #Max player jump width = 47 frames * velocity of moving objects

        with open("data/obstacles.json", "r") as jsonfile:
            self.__obstacles: dict = json.load(jsonfile)


    # Add object to the ObjectHandler.
    def add_object(self, object: Object, moving: bool = False, ground: bool = False, obstacle: bool = False):
        self.obh.objects.append(object)
        if moving:
            self.obh.add_moving(object)
        if ground:
            self.obh.add_ground(object)
        if obstacle:
            self.obh.add_obstacle(object)
    
    def add_obstacle(self, object: Object, moving: bool = True, ground: bool = True, obstacle: bool = True):
        self.add_object(object, moving, ground, obstacle)
        self.gen_objs.append(object)

    def handle_generation(self, obh):
        for obj in self.gen_objs:
            if obj not in self.obh.objects:
                self.gen_objs.remove(obj)

        dx, dy = pygame.display.get_surface().get_size()

        if self.obh.player is not None:
            fx, fy, fw, fh = self.obh.floor.get_rect()

            spawn_left: int = dx
            spawn_top: int = fy - fh
            spawn_w: int = 200
            spawn_h: int = 50

            if self.__last_formation != None:
                spawn_left = self.__last_formation.right()
                spawn_top = self.__last_formation.top()
            
            if spawn_left <= dx:
                self.gen_random_obstacle(spawn_left, spawn_top, spawn_w, spawn_h)

            # if self.obh.player_floored and self.gen_objs == []:
            #     #Create a staircase to endanger the player
            #     colour = (255, 255, 255)

            #     obj = Object((x, fy - h, w, h), colour)
            #     obj2 = Object((x + w, fy - (h * 2), w, h), colour)
            #     obj3 = Object((x + (w * 2), fy - (h * 3), w, h), colour)
            #     obj4 = Object((x + (w * 3), fy - (h * 4), w, h), colour)

            #     self.gen_objs = [obj, obj2, obj3, obj4]

            #     self.add_object(obj, True, True, True)
            #     self.add_object(obj2, True, True, True)
            #     self.add_object(obj3, True, True, True)
            #     self.add_object(obj4, True, True, True)

            #     x = x + (w * 4) #So that the next generated object is after obj4...
            #     y = fy - (h * 4) #...and in line with it.

            #     self.random_obstacle(x, y, w, h, 50)

            # elif self.obh.player_floored_cnt > 0 and self.last_obj_type != "DOWN_STAIR":

            #     print(self.last_obj_type)

            #     if last_obj_x < dx:
            #         applied_x = last_obj_x + w
            #         x = self.get_obstacle_type(applied_x - 5, last_obj_y, w, h, 50)
            #         y = last_obj_y

            #         if self.last_obj_type != "DOWN_STAIR": #Catches any "DOWN_STAIR" object types created in the IF statement above

            #             first_obj = Object((x, y, w, h), (255, 255, 0))
            #             self.add_object(first_obj, True, True, True)
            #             self.gen_objs.append(first_obj)

            #             colour = (0, 255, 255)
                
            #             gen_num = 5 #This should always be odd to ensure the next loop works correctly (the midpoint should be an integer)
            #             midpt = statistics.median(range(gen_num))

            #             obj_arr = np.zeros((gen_num, gen_num)) #Creates a gen_num by gen_num grid of zeroes
            #             #This will be used to show whether a coordinate is occupied or not, and will be used to determine the next object's position.

            #             #The middle of a (gen_num) indexed array so that the array can represent negative values of displacement
            #             a_x = 0 #The array will represent x values correctly already
            #             a_y = midpt #The array acts as a gen_num x gen_num grid of potential objects
                
            #             deltaY = 0

            #             for i in range(gen_num):

            #                 if i >= midpt:
            #                     if a_y - midpt + gen_num < 0:
            #                         deltaY = -1 #To make this obstacle formation possible, y must go back to the starting point

            #                 #Convert a_y into true displacement by subtracting midpt from it
            #                 if a_y == gen_num - 1:
            #                     deltaY = -1

            #                 elif a_y == 0:
            #                     deltaY = 1
                            
            #                 else:
            #                     deltaY = random.randint(-1,1) #Whether the y coordinate will go up, down or not change.

            #                 a_y += deltaY
            #                 obj_arr[a_y][a_x] = 1
            #                 a_x += 1

            #                 generatedObjects = {}

            #                 g_index_y = -midpt

            #                 for row in obj_arr:
            #                     g_index_x = 0
            #                     vals = []
            #                     for val in row:
            #                         if val == 1:
            #                             vals.append(g_index_x)
                           
            #                         g_index_x += 1

            #                     generatedObjects.update({g_index_y: vals})
            #                     g_index_y += 1

            #                 for obj in generatedObjects:
            #                     for val in generatedObjects[obj]:
            #                         o = Object((x + w + (w * val-1), y + (h * obj), w, h), colour)
            #                         self.add_object(o, True, True, True)
            #                         self.gen_objs.append(o) 

            #             x = first_obj.get_left() + (w * gen_num)

            #             last_obj = Object((x + w, last_obj_y, w, h), (255, 0, 255))
            #             self.add_object(last_obj, True, True, True)
            #             self.gen_objs.append(last_obj)
    

    def gen_random_obstacle(self, left: int, top: int, w: int, h: int):
        # Get random formation
        obstacle = self.__obstacles["formations"][random.randrange(0, len(self.__obstacles["formations"]))]
        formation = obstacle["formation"]
        print(obstacle["name"])

        t_row = ObstacleRow([])

        m_row = ObstacleRow([])
        if formation[0][0] == "x":
            tl = Object(pygame.Rect(left, top - h, w, h), Colour.yellow)
            self.add_obstacle(tl, True, True, True)
            m_row.append(tl)
        if formation[0][1] == "x":
            tr = Object(pygame.Rect(left + w, top - h, w, h), Colour.yellow)
            self.add_obstacle(tr, True, True, True)
            m_row.append(tr)

        b_row = ObstacleRow([])
        if formation[1][0] == "x":
            bl = Object(pygame.Rect(left, top, w, h), Colour.yellow)
            self.add_obstacle(bl, True, True, True)
            b_row.append(bl)
        if formation[1][1] == "x":
            br = Object(pygame.Rect(left + w, top, w, h), Colour.yellow)
            self.add_obstacle(br, True, True, True)
            b_row.append(br)
        
        self.__last_formation = ObstacleMatrix([t_row,
                                                m_row,
                                                b_row])