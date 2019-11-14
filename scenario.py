import pygame
from pygame.locals import *

class Scenario:
  def __init__(self, title):
    self.title = title
    self.display = (500, 500)
    self.surface = None
    self.objects = {}
    #A dictionary of objects, defined by a tuple of (x, y, w, h)
    self.is_running = True
    
  def on_init():
    pygame.init()
    self.surface = 
    
  def set_title(self, new_title):
    self.title = new_title
    
  def get_title(self):
    return self.title
