import numpy as np
from pygameWindow import PYGAME_WINDOW
import constants

def Perturb_Circle_Position():
    global x,y
    fourSidedDieRoll = np.random.randint(4)+1
    if fourSidedDieRoll==1:
        x-=constants.circleVelocity
    elif fourSidedDieRoll==2:
        x+=constants.circleVelocity
    elif fourSidedDieRoll==3:
        y-=constants.circleVelocity
    elif fourSidedDieRoll==4:
        y+=constants.circleVelocity
    else:
        print("Warning. fourSidedDieRoll is not in [1,4].")

pygameWindow = PYGAME_WINDOW()
x = constants.pygameWindowWidth/2
y = constants.pygameWindowDepth/2


while(True):
    pygameWindow.Prepare()
    pygameWindow.DrawBlackCircles(x, y)
    Perturb_Circle_Position()
    pygameWindow.Reveal()
#    print('Draw something.')

