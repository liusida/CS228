from pygameWindow_Del03 import PYGAME_WINDOW
import constants
import sys
sys.path.insert(0, '../LeapSDK/lib')
sys.path.insert(0, '../LeapSDK/lib/x86')
import Leap

class DELIVERABLE:
    def __init__(self):
        self.controller = Leap.Controller()
        self.pygameWindow = PYGAME_WINDOW()
        self.x = constants.pygameWindowWidth/2
        self.y = constants.pygameWindowDepth/2
        self.xMin, self.xMax, self.yMin, self.yMax = (0,0,0,0)
        self.stretching = False
        self.numberOfHands = 0

    def Handle_Finger(self, finger):
        for b in range(4):
            bone = finger.bone(b)
            self.Handle_Bone(bone)

    def Handle_Bone(self, bone):
        base = bone.prev_joint
        tip = bone.next_joint
        self.pygameWindow.Draw_Black_Line(self.Handle_Vector_From_Leap(base), \
            self.Handle_Vector_From_Leap(tip), 4-bone.type)

    def Handle_Vector_From_Leap(self, v):
        global xMin, xMax, yMin, yMax
        global stretching
        x=v.x
        y=v.z
        if (x<self.xMin):
            self.xMin = x
            self.stretching = True
        if (x>self.xMax):
            self.xMax = x
            self.stretching = True
        if (y<self.yMin):
            self.yMin = y
            self.stretching = True
        if (y>self.yMax):
            self.yMax = y
            self.stretching = True
        x = self.Scale(x, self.xMin, self.xMax, 0, constants.pygameWindowWidth)
        y = self.Scale(y, self.yMin, self.yMax, 0, constants.pygameWindowDepth)
        return (x, y)

    def Handle_Frame(self, frame):
        hand = frame.hands[0]
        fingers = hand.fingers
        for finger in fingers:
            self.Handle_Finger(finger)
        
    def Scale(self, value, sourceMin, sourceMax, targetMin, targetMax):
        sourceWidth = sourceMax-sourceMin
        if sourceWidth==0:
            sourceWidth = 1
        targetWidth = targetMax-targetMin
        sourceOffset = value-sourceMin

        return sourceOffset * targetWidth / sourceWidth + targetMin

    def Run_Once(self):
        self.pygameWindow.Prepare()
        self.stretching = False
        frame = self.controller.frame()
        if (len(frame.hands)>0):
            self.Handle_Frame(frame)
        self.pygameWindow.Reveal()

    def Run_Forever(self):
        while(True):
            self.Run_Once()

