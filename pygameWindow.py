import pygame
import sys
import constants

class PYGAME_WINDOW:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.pygameWindowWidth, constants.pygameWindowDepth))
        self.last_status = ''
        pygame.font.init()

    def Text(self, text="hello", color=(0,0,0), size=40, position=(0,0), align='left'):
        font = pygame.font.SysFont('Times New Roman', size)
        textsurface = font.render(text, False, color)
        if align=='right':
            textsurface.get_rect().right = 0
        self.screen.blit(textsurface,position)

    def Prepare(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        white = 255,255,255
        self.screen.fill(white)
        pygame.draw.rect( self.screen, (240,240,240), (0, 0, constants.pygameWindowWidth/2, constants.pygameWindowDepth/2 ))
        pygame.draw.rect( self.screen, (250,250,250), (constants.pygameWindowWidth/2, constants.pygameWindowDepth/2, constants.pygameWindowWidth, constants.pygameWindowDepth ))

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
    
    def Draw_Circle(self, color, center, radius, width=0):
        pygame.draw.circle(self.screen, color, center, radius)

    def Print(self, status):
        font = pygame.font.SysFont("consolas", 16)
        text = font.render(str(status), True, (255,0,0))
        self.screen.blit(text, (5,constants.pygameWindowDepth-text.get_height()))

    def DrawImg(self, img, position):
        self.screen.blit(img, position)

    def LoadImg(self, fname, resize=None):
        ret = pygame.image.load(fname)
        if resize is not None:
            ret = pygame.transform.scale(ret, resize)
        return ret

if __name__ == "__main__":
    w = PYGAME_WINDOW()
    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        w.Prepare()
        w.Print("test")
        w.Reveal()
