from pygameWindow import PYGAME_WINDOW
import constants

pygameWindow = PYGAME_WINDOW()

while(True):
    pygameWindow.Prepare()
    center_x = constants.pygameWindowWidth/2
    center_y = constants.pygameWindowDepth/2

    pygameWindow.DrawBlackCircles(center_x, center_y)

    pygameWindow.Reveal()
#    print('Draw something.')

