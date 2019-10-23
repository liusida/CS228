import numpy as np
from pygameWindow import PYGAME_WINDOW
import constants

import sys
sys.path.insert(0, '../LeapSDK/lib')
sys.path.insert(0, '../LeapSDK/lib/x86')
import Leap

controller = Leap.Controller()



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

def Handle_Frame(frame):
    global x,y
    global xMin, xMax, yMin, yMax
    global stretching
    hand = frame.hands[0]
    fingers = hand.fingers
    indexFingerList = fingers.finger_type(Leap.Finger.TYPE_INDEX)
    indexFinger = indexFingerList[0]
    distalPhalanx = indexFinger.bone(Leap.Bone.TYPE_DISTAL)
    tip = distalPhalanx.next_joint
    x=tip[0]
    y=tip[1]
    stretching = False
    if (x<xMin):
        xMin = x
        stretching = True
    if (x>xMax):
        xMax = x
        stretching = True
    if (y<yMin):
        yMin = y
        stretching = True
    if (y>yMax):
        yMax = y
        stretching = True

def Scale(value, sourceMin, sourceMax, targetMin, targetMax):
    sourceWidth = sourceMax-sourceMin
    if sourceWidth==0:
        sourceWidth = 1
    targetWidth = targetMax-targetMin
    sourceOffset = value-sourceMin

    return sourceOffset * targetWidth / sourceWidth + targetMin



pygameWindow = PYGAME_WINDOW()
x = constants.pygameWindowWidth/2
y = constants.pygameWindowDepth/2

xMin, xMax, yMin, yMax = (0,0,0,0)

stretching = False

while(True):
    pygameWindow.Prepare()

    frame = controller.frame()
    if (len(frame.hands)>0):
        Handle_Frame(frame)

    pygameX = Scale(x, xMin, xMax, 0, constants.pygameWindowWidth)
    pygameY = Scale(y, yMin, yMax, constants.pygameWindowDepth, 0)

    if stretching:
        pygameWindow.Fill((220,220,220))
    pygameWindow.Print("xMin:"+str(xMin)+" xMax:"+str(xMax)+" x:"+str(x)+" pygameX:"+str(pygameX))
    pygameWindow.Draw_Black_Circles(pygameX, pygameY)
    #Perturb_Circle_Position()
    pygameWindow.Reveal()
#    print('Draw something.')

