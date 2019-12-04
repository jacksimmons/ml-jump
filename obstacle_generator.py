import random
import math
import pygame

class ObjectGenerator:
	def __init__(self, obh):
		self.obh = obh #The ObjectHandler that instantiated this object

		#Max player jump height = 109 pixels
		#Max player jump width = 47 frames * velocity of moving objects
	
	def generate_obstacle(self, obh):

		dx, dy = pygame.display.get_surface().get_size()

		player = self.obh.get_player()
		
		if player is not None:

			px, py, pw, ph = player.get_rect()

			if obh.player_grounded:
				print(obh.get_moving())
				if obh.get_moving() == []:

					colour = (255, 255, 255)
					w, h = 185, 50

					obj = obh.create_object((800, py - ph, w, h), colour)
					obh.add_object(obj)
					obh.add_moving(obj)
					obh.add_ground(obj)

					obj2 = obh.create_object((800 + w, py - (ph + h), w, h), colour)
					obh.add_object(obj2)
					obh.add_moving(obj2)
					obh.add_ground(obj2)

					obj3 = obh.create_object((800 + (w * 2), py - (ph + h * 2), w, h), colour)
					obh.add_object(obj3)
					obh.add_moving(obj3)
					obh.add_ground(obj3)

					obj4 = obh.create_object((800 + (w * 3), py - (ph + h * 3), w, h), colour)
					obh.add_object(obj4)
					obh.add_moving(obj4)
					obh.add_ground(obj4)