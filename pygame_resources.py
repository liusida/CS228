import pygame
from lib import constants, pygame_textinput

# images
img = {}
img_pos = {}

img["hand_2"] = pygame.image.load('images/vhand_2.png')
img["hand_3"] = pygame.image.load('images/vhand_3.png')
img["hand_g"] = pygame.image.load('images/vhand_g.png')

img["sensor"] = pygame.image.load('images/sensor_t.png')

green_x = constants.pygameWindowWidth - 40
green_y = 60
green_size = 30

img["asl_small"] = []
img["asl"] = []
for i in range(10):
    d = pygame.image.load('images/ASL/%d.png' % i)
    d = pygame.transform.scale(d, (140, 224))
    img["asl"].append(d)

    img["asl_small"].append(pygame.image.load('images/ASL/%d.png' % i))

d = pygame.image.load('images/back_img.png')
img["back_img"] = pygame.transform.scale(
    d, (constants.pygameWindowWidth / 2, constants.pygameWindowDepth / 2))

img["success"] = pygame.image.load('images/success.png')

# fonts
font = {}
font["login_title"] = pygame.font.Font(pygame.font.match_font('Arial'), 40)
font["login_name"] = pygame.font.Font(pygame.font.match_font('Arial'), 20)
font["digit_large"] = pygame.font.Font(pygame.font.match_font('Arial'), 60)

# inputs
inputs = {}
inputs["username"] = pygame_textinput.TextInput(font_family="Arial",
                                                font_size=20)

# positions
img_pos["asl_x"] = constants.divide_x + (
    constants.pygameWindowWidth -
    constants.divide_x) / 2 - img["asl"][0].get_width() / 2
img_pos["asl_y"] = constants.divide_y + (
    constants.pygameWindowDepth -
    constants.divide_y) / 2 - img["asl"][0].get_height() / 2

img_pos["sensor_x"] = constants.divide_x + (
    constants.pygameWindowWidth -
    constants.divide_x) / 2 - img["sensor"].get_width() / 2
img_pos[
    "sensor_y"] = constants.divide_y / 2 - img["sensor"].get_height() / 2 + 80

img_pos["hand_x"] = constants.divide_x + (
    constants.pygameWindowWidth -
    constants.divide_x) / 2 - img["hand_2"].get_width() / 2
img_pos[
    "hand_y"] = constants.divide_y / 2 - img["hand_2"].get_height() / 2 - 80

img_pos["asl_digit_x"] = constants.divide_x + (constants.pygameWindowWidth -
                                               constants.divide_x) / 2 - 20
img_pos["asl_digit_y"] = constants.divide_y + 50

img_pos["success_x"] = constants.pygameWindowWidth
img_pos["success_y"] = 5