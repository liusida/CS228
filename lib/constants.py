import pygame

pygameWindowWidth = 900
pygameWindowDepth = 800

pygameCircleRadius = 16

circleVelocity = 1

xMin, xMax, yMin, yMax = (-1000, 1000, -1000, 1000)

divide_x = pygameWindowWidth / 2
divide_y = pygameWindowDepth / 2

PY_ANIMATION_EVENT = pygame.USEREVENT + 0
PY_CORRECT_DIGIT = pygame.USEREVENT + 1

success_needed_for_unlock_new_digit = 2
