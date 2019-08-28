import pygame
import sys
import constants

class PYGAME_WINDOW:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.pygameWindowWidth, constants.pygameWindowDepth))

    def Prepare(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        white = 255,255,255
        self.screen.fill(white)

    def Reveal(self):
        pygame.display.update()

    def DrawBlackCircles(self, x, y):
        black = 0,0,0
        pygame.draw.circle(self.screen, black, (x,y), constants.pygameCircleRadius)
