import random
import math
import pygame

class ObjectGenerator:
	def __init__(self, obh):
		self.obh = obh #The ObjectHandler that instantiated this object
		self.gen_objs = [] #All of the generated objects currently on screen
		self.formations = ["Spike", "Dip", "Staircase"] #To make the generation easier to understand

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

	def handle_generation(self, obh):
		print(self.obh.player_floored)
		for obj in self.gen_objs:
			if obj not in self.obh.objects:
				self.gen_objs.remove(obj)

		dx, dy = pygame.display.get_surface().get_size()

		if self.obh.player is not None:
			px, py, pw, ph = obh.player.get_rect()

			x, w, h = 800, 185, 50
			y = py - ph

			if self.gen_objs == []:

				if self.obh.player_floored:
					#Create a staircase to endanger the player
					colour = (255, 255, 255)

					obj = obh.create_object((x, py - ph, w, h), colour)
					obj2 = obh.create_object((x + w, py - (ph + h), w, h), colour)
					obj3 = obh.create_object((x + (w * 2), py - (ph + h * 2), w, h), colour)
					obj4 = obh.create_object((x + (w * 3), py - (ph + h * 3), w, h), colour)

					self.gen_objs = [obj, obj2, obj3, obj4]

					self.ao(obj, True, True, True)
					self.ao(obj2, True, True, True)
					self.ao(obj3, True, True, True)
					self.ao(obj4, True, True, True)

					x = x + (w * 4) #So that the next generated object is after obj4...
					y = py - (ph + h * 3) #...and in line with it.
                    
                for x in range(5): #Create landscape in groups of 5
                    in_loop = True
                    if in_loop:
                        r = random.choice(self.formations)

                        if r == "Spike":
                            #This is a basic obstacle, which the player must jump over
                            colour = (255, 0, 0)
                            gnd = obh.create_object((x, y, w/3, h), colour)
                            gnd2 = obh.create_object((x + w/3, y, w/3, h), colour)
                            gnd3 = obh.create_object((x + (w/3 * 2), y, w/3, h), colour)

                            spike = obh.create_object((x + w/3, y - h, w/3, h), colour)
                            self.ao(gnd, True, True, True)
                            self.ao(gnd2, True, True, True)
                            self.ao(gnd3, True, True, True)
                            self.ao(spike, True, False, True)

                            self.gen_objs.append(gnd)
                            self.gen_objs.append(gnd2)
                            self.gen_objs.append(gnd3)
                            self.gen_objs.append(spike)

                            x = x + (w * 3) #For most formations, y displacement = 0.

                        elif r == "Dip":
                            #This is a 'Dip' where the player must go down and then back up
                            colour = (0, 255, 0)
                            #Where y = starting y
                            gnd = obh.create_object((x, y, w, h), colour)
                            gnd2 = obh.create_object((x + (w * 6), y, w, h), colour)
                            dip = obh.create_object((x + (w * 3), y, w, h), colour)

                            #Where y < starting y and is decreasing:
                            gndd1 = obh.create_object((x + w, y + h, w, h), colour)
                            gndd2 = obh.create_object((x + (w * 2), y + (h * 2), w, h), colour)
                            gndd3 = obh.create_object((x + (w * 3), y + (h * 3), w, h), colour)

                            #Where y < starting y but is increasing:
                            gndu1 = obh.create_object((x + (w * 4), y + (h * 2), w, h), colour)
                            gndu2 = obh.create_object((x + (w * 5), y + h, w, h), colour)

                            self.ao(gnd, True, True, True)
                            self.gen_objs.append(gnd)
                            self.ao(gnd2, True, True, True)
                            self.gen_objs.append(gnd2)
                            self.ao(dip, True, False, True)
                            self.gen_objs.append(dip)

                            self.ao(gndd1, True, True, True)
                            self.gen_objs.append(gndd1)
                            self.ao(gndd2, True, True, True)
                            self.gen_objs.append(gndd2)
                            self.ao(gndd3, True, True, True)
                            self.gen_objs.append(gndd3)

                            self.ao(gndu1, True, True, True)
                            self.gen_objs.append(gndu1)
                            self.ao(gndu2, True, True, True)
                            self.gen_objs.append(gndu2)

                            x = x + (w * 7)

                        elif r == "Staircase":
                            #This is a downwards staircase
                            colour = (0, 0, 255)
                            obj = obh.create_object((x, y, w, h), colour)
                            obj2 = obh.create_object((x + w, y + h, w, h), colour)
                            obj3 = obh.create_object((x + (w*2), y + (h*2), w, h), colour)
                            obj4 = obh.create_object((x + (w*3), y + (h*3), w, h), colour)

                            self.gen_objs = [obj, obj2, obj3, obj4]

                            self.ao(obj, True, True, True)
                            self.ao(obj2, True, True, True)
                            self.ao(obj3, True, True, True)
                            self.ao(obj4, True, True, True)

                            x = x + (w * 4) #So that the next generated object is after obj4...
                            in_loop = False
                    else:
                        break
