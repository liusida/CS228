import pygame
import pygame_textinput

import sys
import constants
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "0,22"

class PYGAME_WINDOW:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((constants.pygameWindowWidth, constants.pygameWindowDepth))
        self.last_status = ''
        pygame.font.init()
        self.textinput = pygame_textinput.TextInput(font_family="Arial", font_size=20)
        self.back_img = self.LoadImg(fname='images/back_img.png', resize=(constants.pygameWindowWidth/2,constants.pygameWindowDepth/2))

    def Text(self, text="hello", color=(0,0,0), size=40, position=(0,0)):
        font = pygame.font.Font(pygame.font.match_font('Arial'), size)
        textsurface = font.render(text, True, color)
        self.screen.blit(textsurface, position)

    def Input(self, events, text="Sida", position=(0,0)):
        ret = self.textinput.update(events)
        self.screen.blit(self.textinput.get_surface(), position)
        return ret

    def Prepare(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                return -1
        white = 255,255,255
        self.screen.fill(white)
        return events

    def SeparateWindows(self):
        self.screen.blit(self.back_img, (0,0))
        #pygame.draw.rect( self.screen, (240,240,240), (0, 0, constants.pygameWindowWidth/2, constants.pygameWindowDepth/2 ))
        width = 1
        color = (124,124,124)
        pygame.draw.line(self.screen, color, (0,constants.pygameWindowDepth/2), (constants.pygameWindowWidth,constants.pygameWindowDepth/2), width)
        pygame.draw.line(self.screen, color, (constants.pygameWindowWidth/2,0), (constants.pygameWindowWidth/2,constants.pygameWindowDepth), width)
        #pygame.draw.rect( self.screen, (250,250,250), (0, constants.pygameWindowDepth/2, constants.pygameWindowWidth/2, constants.pygameWindowDepth ))
        #pygame.draw.rect( self.screen, (250,250,250), (constants.pygameWindowWidth/2, constants.pygameWindowDepth/2, constants.pygameWindowWidth, constants.pygameWindowDepth ))

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
        w.SeparateWindows()
        w.Print("test")
        w.Reveal()
