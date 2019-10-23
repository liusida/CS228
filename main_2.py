import os
import numpy as np
import pickle
import pygame

import game_logic
from lib import constants, standardization, show, pickle_database, pygame_textinput
from lib.knn import KNN

import sys
sys.path.insert(0, '../LeapSDK/lib')
sys.path.insert(0, '../LeapSDK/lib/x86')
import Leap  # Leap Motion SDK

os.environ['SDL_VIDEO_WINDOW_POS'] = "500,22"  # place of initial window

# pygame initialization
pygame.init()
pygame.font.init()
pygame_screen = pygame.display.set_mode(
    (constants.pygameWindowWidth, constants.pygameWindowDepth))
pygame_events = None
clock = pygame.time.Clock()
pygame.time.set_timer(constants.PY_ANIMATION_EVENT, 50)

# Leap Motion initialization
controller = Leap.Controller()

# Logic Initialization
game_logic.Init()

# global variables
programState = -1  # so-called "state programming".
isRunning = True

# main loop
while (isRunning):
    pygame.display.update()
    clock.tick_busy_loop(60)
    pygame_screen.fill((255, 255, 255))
    pygame_events = pygame.event.get()
    for event in pygame_events:
        if event.type == pygame.QUIT:
            isRunning = False

    game_logic.Game_Logic(pygame_screen, pygame_events, controller)

# before exiting
pygame.display.quit()
pygame.quit()
