import pygame
import sys
import constants

class PYGAME_WINDOW:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.pygameWindowWidth, constants.pygameWindowDepth))
        self.last_status = ''

    def Prepare(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        white = 255,255,255
        self.screen.fill(white)

    def Fill(self, color):
        self.screen.fill(color)

    def Reveal(self):
        pygame.display.update()

    def Draw_Black_Circles(self, x, y):
        black = 0,0,0
        pygame.draw.circle(self.screen, black, (int(x),int(y)), constants.pygameCircleRadius)

    def Draw_Black_Line(self, base, tip, width=2):
        black = 0,0,0
        pygame.draw.line(self.screen, black, base, tip, width)

    def Print(self, status):
        font = pygame.font.SysFont("consolas", 16)
        text = font.render(str(status), True, (255,0,0))
        self.screen.blit(text, (5,constants.pygameWindowDepth-text.get_height()))


if __name__ == "__main__":
    w = PYGAME_WINDOW()
    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        w.Prepare()
        w.Print("test")
        w.Reveal()
