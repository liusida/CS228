import sys
import pygame
import os
os.chdir(os.path.dirname(os.path.abspath(__file__))) # enter the right path.

pygame.init()

size = width, height = 1000, 800
speed = [1, 1]
black = 0, 0, 0
white = 255,255,255

screen = pygame.display.set_mode(size)

ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(white)
    screen.blit(ball, ballrect)
    pygame.display.flip()