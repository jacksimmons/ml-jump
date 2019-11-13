import pygame

#Initialise pygame
pygame.init()

#Create a display window

wx = 1000 #Display's x dimension
wy = 1000 #Display's y dimension

splitx = 100 #The x coordinate of the line separating the main window and the dev console

disp = pygame.display.set_mode((wx, wy))
pygame.display.set_caption("Title Screen")

#Initialise fonts
font = pygame.font.SysFont('Bahnschrift', 30)

x = 50
y = 50
w = 50
h = 50

v = 5

dim = 60, 40

black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255

rects = {
    'button1': (10,20,30,40) #x, y, w, h
}

#Create a Clock object and limit framerate
clock = pygame.time.Clock()
fps_limit = 60

#Titlescreen loop
title = True
while title:
    clock.tick(fps_limit)

    #Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            title = False
        if event.type == 

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        y -= v

    print(clock.get_time())

    disp.fill(black)
    pygame.draw.line(disp, white, (splitx, wy), (splitx, 0))
    pygame.draw.rect(disp, red, (x, y, w, h))
    font.render('Text', False, white)
    pygame.display.update()

pygame.quit()
