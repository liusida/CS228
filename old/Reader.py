import numpy as np
import pickle
import os
import time
from pygameWindow_Del03 import PYGAME_WINDOW
import constants

class READER:
    def __init__(self):
        self.Get_Gesture_Number()

    def Get_Gesture_Number(self):
        path, dirs, files = next(os.walk('userData'))
        self.numGesture = len(files)

    def Print_Gestures(self):
        for i in range(self.numGesture):
            pickle_in = open("userData/gesture%d.p"%i,"rb")
            gestureData = pickle.load(pickle_in)
            pickle_in.close()
            print(gestureData[0,0,0])

    def Draw_Gestures(self):
        assert(self.numGesture>0)

        self.pygameWindow = PYGAME_WINDOW()
        while(True):
            self.Draw_Each_Gesture_Once()
    
    def Draw_Gesture(self, gestureIndex):
        self.pygameWindow.Prepare()

        pickle_in = open("userData/gesture%d.p"%gestureIndex,"rb")
        gestureData = pickle.load(pickle_in)
        pickle_in.close()
        
        for i in range(5):
            for j in range(4):
                currentBone = gestureData[i,j,:]
                xBaseNotYetScaled = currentBone[0]
                yBaseNotYetScaled = currentBone[2]
                xTipNotYetScaled = currentBone[3]
                yTipNotYetScaled = currentBone[5]
                xBase = self.Scale(xBaseNotYetScaled, constants.xMin, constants.xMax, 0, constants.pygameWindowWidth)
                yBase = self.Scale(yBaseNotYetScaled, constants.yMin, constants.yMax, 0, constants.pygameWindowDepth)
                xTip = self.Scale(xTipNotYetScaled, constants.xMin, constants.xMax, 0, constants.pygameWindowWidth)
                yTip = self.Scale(yTipNotYetScaled, constants.yMin, constants.yMax, 0, constants.pygameWindowDepth)
                self.pygameWindow.Draw_Line((xBase,yBase),(xTip,yTip),color=(0,0,255))

        self.pygameWindow.Reveal()
        time.sleep(0.3)

    def Scale(self, value, sourceMin, sourceMax, targetMin, targetMax):
        sourceWidth = sourceMax-sourceMin
        if sourceWidth==0:
            sourceWidth = 1
        targetWidth = targetMax-targetMin
        sourceOffset = value-sourceMin

        return sourceOffset * targetWidth / sourceWidth + targetMin

    def Draw_Each_Gesture_Once(self):
        for i in range(self.numGesture):
            self.Draw_Gesture(i)



if __name__ == "__main__":
    Reader = READER()
    Reader.Draw_Gestures()