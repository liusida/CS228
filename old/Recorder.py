import numpy as np
import pickle
from pygameWindow_Del03 import PYGAME_WINDOW
import constants
import sys
sys.path.insert(0, '../LeapSDK/lib')
sys.path.insert(0, '../LeapSDK/lib/x86')
import Leap
import os, glob

class RECORDER:
    def __init__(self):
        self.numberOfGestures = 1000
        self.gestureIndex = 0

        self.controller = Leap.Controller()
        self.pygameWindow = PYGAME_WINDOW()
        self.x = constants.pygameWindowWidth/2
        self.y = constants.pygameWindowDepth/2
        self.xMin, self.xMax, self.yMin, self.yMax = (0,0,0,0)
        self.stretching = False
        self.previousNumberOfHands = 0
        self.currentNumberOfHands = 0

        self.gestureData = np.zeros((5,4,6,self.numberOfGestures), dtype='f')

        self.pickleFileIndex = 0
        self.Delete_All_UserData()

    def Delete_All_UserData(self):
        userPath = os.path.dirname(os.path.realpath(__file__))+"/userData"
        if os.path.exists(userPath):
            fileList = glob.glob(userPath+"/gesture*.p")
            for f in fileList:
                os.remove(f)
        else:
            os.mkdir(userPath)
        
    def Handle_Finger(self, finger):
        for b in range(4):
            bone = finger.bone(b)
            self.Handle_Bone(bone, finger.type, b)

    def Handle_Bone(self, bone, i, j):
        base = bone.prev_joint
        tip = bone.next_joint

        if (self.currentNumberOfHands==1):
            color = 0,255,0
        elif (self.currentNumberOfHands==2):
            color = 255,0,0
        else:
            color = 0,0,255

        self.pygameWindow.Draw_Line(self.Handle_Vector_From_Leap(base), \
            self.Handle_Vector_From_Leap(tip), 4-bone.type, color)
        
        # store all data
        if self.currentNumberOfHands == 2:
            self.gestureData[i,j,0,self.gestureIndex] = base.x
            self.gestureData[i,j,1,self.gestureIndex] = base.y
            self.gestureData[i,j,2,self.gestureIndex] = base.z
            self.gestureData[i,j,3,self.gestureIndex] = tip.x
            self.gestureData[i,j,4,self.gestureIndex] = tip.y
            self.gestureData[i,j,5,self.gestureIndex] = tip.z

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
        # because the device is unstable, so sometimes it will tell you there are two hands, and next second it will tell you there's only one.
        # That's why the live demo in class is not doing very well.
        self.currentNumberOfHands = len(frame.hands)
        hand = frame.hands[0]
        fingers = hand.fingers
        for finger in fingers:
            self.Handle_Finger(finger)
        if self.currentNumberOfHands==2:
            print('gesture ' + str(self.gestureIndex) + ' stored.')
            self.gestureIndex = self.gestureIndex + 1
            if self.gestureIndex == self.numberOfGestures:
                self.Save_Gesture()
                exit(0)
    
    def Save_Gesture(self):
        pickle_out = open("userData/gesture.p","wb")
        pickle.dump(self.gestureData, pickle_out)
        pickle_out.close()
        #self.pickleFileIndex += 1

    def Scale(self, value, sourceMin, sourceMax, targetMin, targetMax):
        sourceWidth = sourceMax-sourceMin
        if sourceWidth==0:
            sourceWidth = 1
        targetWidth = targetMax-targetMin
        sourceOffset = value-sourceMin

        return sourceOffset * targetWidth / sourceWidth + targetMin

    def Recording_is_Ending(self):
        return (self.previousNumberOfHands==2 and self.currentNumberOfHands==1)

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
            self.previousNumberOfHands = self.currentNumberOfHands

if __name__ == "__main__":
    r = RECORDER()
    r.Run_Forever()
    exit()