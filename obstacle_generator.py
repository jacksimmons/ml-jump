import random
import math
import pygame
import statistics

import numpy as np

class ObjectGenerator:
    def __init__(self, obh):
        self.obh = obh #The ObjectHandler that instantiated this object
        self.gen_objs = [] #All of the generated objects currently on screen
        self.last_obj_type = None #The type of obstacle/ground last generated

        #Max player jump height = 109 pixels
        #Max player jump width = 47 frames * velocity of moving objects

    def ao(self, object, moving:bool=False, ground:bool=False, obstacle:bool=False): #Add an object to the ObjectHandler (for simplicity)
        self.obh.objects.append(object)
        if moving:
            self.obh.moving.append(object)
        if ground:
            self.obh.ground.append(object)
        if obstacle:
            self.obh.obstacles.append(object)

    def get_obstacle_type(self, x, y, w, h, sw): #sw - Small width for smaller obstacles
        r = random.randint(0, 100)

        if r in range(0, 44):
            #This is a basic obstacle, which the player must jump over
            colour = (255, 0, 0)
            gnd = self.obh.create_object((x, y, sw, h), colour)
            gnd2 = self.obh.create_object((x + sw, y, sw, h), colour)
            spike = self.obh.create_object((x + sw, y - h, 50, h), colour)
            gnd3 = self.obh.create_object((x + (sw*2), y, w, h), colour)

            self.ao(gnd, True, True, True)
            self.ao(gnd2, True, True, True)
            self.ao(spike, True, False, True)
            self.ao(gnd3, True, True, True)

            self.gen_objs.append(gnd)
            self.gen_objs.append(gnd2)
            self.gen_objs.append(spike)
            self.gen_objs.append(gnd3)

            self.last_obj_type = "SPIKE"

            x += (sw*2) + w

        elif r in range(45, 89):
            #This is a 'Dip' where the player must go down and then back up
            colour = (0, 255, 0)
            #Where y = starting y
            gnd = self.obh.create_object((x, y, w, h), colour)
            gnd2 = self.obh.create_object((x + (w * 6), y, w, h), colour)
            dip = self.obh.create_object((x + (w * 3) + (w/2 - sw/2), y, sw, h), colour)

            #Where y < starting y and is decreasing:
            gndd1 = self.obh.create_object((x + w, y + h, w, h), colour)
            gndd2 = self.obh.create_object((x + (w * 2), y + (h * 2), w, h), colour)
            gndd3 = self.obh.create_object((x + (w * 3), y + (h * 3), w, h), colour)

            #Where y < starting y but is increasing:
            gndu1 = self.obh.create_object((x + (w * 4), y + (h * 2), w, h), colour)
            gndu2 = self.obh.create_object((x + (w * 5), y + h, w, h), colour)

            self.ao(gnd, True, True, True)
            self.gen_objs.append(gnd)

            self.ao(gndd1, True, True, True)
            self.gen_objs.append(gndd1)
            self.ao(gndd2, True, True, True)
            self.gen_objs.append(gndd2)
            self.ao(gndd3, True, True, True)
            self.gen_objs.append(gndd3)

            self.ao(dip, True, False, True)
            self.gen_objs.append(dip)

            self.ao(gndu1, True, True, True)
            self.gen_objs.append(gndu1)
            self.ao(gndu2, True, True, True)
            self.gen_objs.append(gndu2)

            self.ao(gnd2, True, True, True)
            self.gen_objs.append(gnd2)

            self.last_obj_type = "DIP"

            x += (w * 7)

        elif r in range(90, 100):
            #This is a downwards staircase
            colour = (0, 0, 255)
            obj = self.obh.create_object((x, y, w, h), colour)
            obj2 = self.obh.create_object((x + w, y + h, w, h), colour)
            obj3 = self.obh.create_object((x + (w*2), y + (h*2), w, h), colour)
            obj4 = self.obh.create_object((x + (w*3), y + (h*3), w, h), colour)

            self.gen_objs.append(obj)
            self.gen_objs.append(obj2)
            self.gen_objs.append(obj3)
            self.gen_objs.append(obj4)

            self.ao(obj, True, True, True)
            self.ao(obj2, True, True, True)
            self.ao(obj3, True, True, True)
            self.ao(obj4, True, True, True)

            self.last_obj_type = "DOWN_STAIR"

            x += (w * 4) #So that the next generated object is after obj4...

        return x

    def handle_generation(self, obh):
        for obj in self.gen_objs:
            if obj not in self.obh.objects:
                self.gen_objs.remove(obj)

        dx, dy = pygame.display.get_surface().get_size()

        if self.obh.player is not None:
            fx, fy, fw, fh = self.obh.floor.get_rect()

            x, w, h = 1300, 185, 50
            y = fy

            if self.gen_objs != []:
                newestObj = self.gen_objs[len(self.gen_objs)-1]
                last_obj_x, last_obj_y = newestObj.get_x(), newestObj.get_y()
            else:
                last_obj_x, last_obj_y = x, y

            if self.obh.player_floored and self.gen_objs == []:
                #Create a staircase to endanger the player
                colour = (255, 255, 255)

                obj = self.obh.create_object((x, fy - h, w, h), colour)
                obj2 = self.obh.create_object((x + w, fy - (h * 2), w, h), colour)
                obj3 = self.obh.create_object((x + (w * 2), fy - (h * 3), w, h), colour)
                obj4 = self.obh.create_object((x + (w * 3), fy - (h * 4), w, h), colour)

                self.gen_objs = [obj, obj2, obj3, obj4]

                self.ao(obj, True, True, True)
                self.ao(obj2, True, True, True)
                self.ao(obj3, True, True, True)
                self.ao(obj4, True, True, True)

                x = x + (w * 4) #So that the next generated object is after obj4...
                y = fy - (h * 4) #...and in line with it.

                x = self.get_obstacle_type(x, y, w, h, 50)

            elif self.obh.player_floored_cnt > 0 and self.last_obj_type != "DOWN_STAIR":

                print(self.last_obj_type)

                if last_obj_x < dx:
                    applied_x = last_obj_x + w
                    x = self.get_obstacle_type(applied_x - 5, last_obj_y, w, h, 50)
                    y = last_obj_y

                    if self.last_obj_type != "DOWN_STAIR": #Catches any "DOWN_STAIR" object types created in the IF statement above

                        first_obj = self.obh.create_object((x, y, w, h), (255, 255, 0))
                        self.ao(first_obj, True, True, True)
                        self.gen_objs.append(first_obj)

                        colour = (0, 255, 255)
                
                        gen_num = 5 #This should always be odd to ensure the next loop works correctly (the midpoint should be an integer)
                        midpt = statistics.median(range(gen_num))

                        obj_arr = np.zeros((gen_num, gen_num)) #Creates a gen_num by gen_num grid of zeroes
                        #This will be used to show whether a coordinate is occupied or not, and will be used to determine the next object's position.

                        #The middle of a (gen_num) indexed array so that the array can represent negative values of displacement
                        a_x = 0 #The array will represent x values correctly already
                        a_y = midpt #The array acts as a gen_num x gen_num grid of potential objects
                
                        deltaY = 0

                        for i in range(gen_num):

                            if i >= midpt:
                                if a_y - midpt + gen_num < 0:
                                    deltaY = -1 #To make this obstacle formation possible, y must go back to the starting point

                            #Convert a_y into true displacement by subtracting midpt from it
                            if a_y == gen_num - 1:
                                deltaY = -1

                            elif a_y == 0:
                                deltaY = 1
                            
                            else:
                                deltaY = random.randint(-1,1) #Whether the y coordinate will go up, down or not change.

                            a_y += deltaY
                            obj_arr[a_y][a_x] = 1
                            a_x += 1

                            generatedObjects = {}

                            g_index_y = -midpt

                            for row in obj_arr:
                                g_index_x = 0
                                vals = []
                                for val in row:
                                    if val == 1:
                                        vals.append(g_index_x)
                           
                                    g_index_x += 1

                                generatedObjects.update({g_index_y: vals})
                                g_index_y += 1

                            for obj in generatedObjects:
                                for val in generatedObjects[obj]:
                                    print(val)
                                    o = self.obh.create_object((x + w + (w * val-1), y + (h * obj), w, h), colour)
                                    self.ao(o, True, True, True)
                                    self.gen_objs.append(o) 

                        x = first_obj.get_x() + (w * gen_num)

                        last_obj = self.obh.create_object((x + w, last_obj_y, w, h), (255, 0, 255))
                        self.ao(last_obj, True, True, True)
                        self.gen_objs.append(last_obj)
