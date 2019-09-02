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

def Handle_Finger(finger):
    for b in range(4):
        bone = finger.bone(b)
        Handle_Bone(bone)

def Handle_Bone(bone):
    global pygameWindow
    base = bone.prev_joint
    tip = bone.next_joint
    pygameWindow.Draw_Black_Line(Handle_Vector_From_Leap(base), Handle_Vector_From_Leap(tip), 4-bone.type)

def Handle_Vector_From_Leap(v):
    global xMin, xMax, yMin, yMax
    global stretching
    x=v.x
    y=v.z
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
    x = Scale(x, xMin, xMax, 0, constants.pygameWindowWidth)
    # y = Scale(y, yMin, yMax, constants.pygameWindowDepth, 0)
    y = Scale(y, yMin, yMax, 0, constants.pygameWindowDepth)
    return (x, y)

def Handle_Frame(frame):
    # global x,y
    hand = frame.hands[0]
    fingers = hand.fingers
    for finger in fingers:
        Handle_Finger(finger)
    
    # indexFingerList = fingers.finger_type(Leap.Finger.TYPE_INDEX)
    # indexFinger = indexFingerList[0]
    # distalPhalanx = indexFinger.bone(Leap.Bone.TYPE_DISTAL)
    # tip = distalPhalanx.next_joint
    pass

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

# xMin, xMax, yMin, yMax = (-1000,1000,-1000,1000)
xMin, xMax, yMin, yMax = (0,0,0,0)

stretching = False

while(True):
    pygameWindow.Prepare()

    stretching = False

    frame = controller.frame()
    if (len(frame.hands)>0):
        Handle_Frame(frame)


    if stretching:
        #pygameWindow.Print("Stretching...")
        print("Stretching...")
    # pygameWindow.Print("xMin:"+str(xMin)+" xMax:"+str(xMax)+" x:"+str(x)+" pygameX:"+str(pygameX))
    # pygameWindow.DrawBlackCircles(pygameX, pygameY)
    
    #Perturb_Circle_Position()
    pygameWindow.Reveal()

