import pygame
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "0,22"

import pygame_resources

CUSTOMEVENT_1 = pygame.USEREVENT
CUSTOMEVENT_2 = pygame.USEREVENT + 1

pygame.init()
screen = pygame.display.set_mode((600, 600))


def customevent(font):
    text = "test: %d" % pygame.time.get_ticks()
    textsurface = font.render(text, True, (0, 0, 0))
    fps = c.get_fps()
    print u'FPS: {}'.format(fps)
    return textsurface


def draw_loop():
    textsurface = None
    font = pygame.font.Font(pygame.font.match_font('Arial'), 30)
    s = None
    while (True):
        c.tick(60)
        screen.fill((240, 240, 240))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                return
            if event.type == CUSTOMEVENT_1:
                textsurface = customevent(font)
                s = pygame.Surface((400, 100), pygame.SRCALPHA, 32)
                s = s.convert_alpha()
                x = pygame.time.get_ticks() / 100 % 400
                s.blit(textsurface, (x, 10))
        if s:
            screen.blit(s, (10, 10))

        pygame.display.update()


c = pygame.time.Clock()

timer_resolution = pygame.TIMER_RESOLUTION
print(timer_resolution)

# inserts two custom events into the event queue
pygame.time.set_timer(CUSTOMEVENT_1, 1000)
pygame.time.set_timer(CUSTOMEVENT_2, 2000)

draw_loop()
print("exit.")