import sys
sys.path.insert(0, '../LeapSDK/lib')
sys.path.insert(0, '../LeapSDK/lib/x86')
sys.path.insert(0, '.')
from knn import KNN

import numpy as np
from pygameWindow import PYGAME_WINDOW
import constants
import pickle

import Leap

import standardization
import show

# use standardization
use_standardization = False

if use_standardization:
    clf = pickle.load( open('Del6/userData/classifier_with_standardization.p','rb') )
    testData = np.zeros((5,4,6),dtype='f')
else:
    clf = pickle.load( open('Del6/userData/classifier.p','rb') )
    testData = np.zeros((1,30),dtype='f')


controller = Leap.Controller()

def Handle_Finger(finger):
    global k, testData
    for b in range(4):
        bone = finger.bone(b)
        Handle_Bone(bone)
        if use_standardization:
            testData[finger.type, bone.type, 0] = bone.prev_joint.x
            testData[finger.type, bone.type, 1] = bone.prev_joint.y
            testData[finger.type, bone.type, 2] = bone.prev_joint.z
            testData[finger.type, bone.type, 3] = bone.next_joint.x
            testData[finger.type, bone.type, 4] = bone.next_joint.y
            testData[finger.type, bone.type, 5] = bone.next_joint.z
        else:
            if ((b==0) or (b==3)):
                testData[0,k] = bone.next_joint.x
                testData[0,k+1] = bone.next_joint.y
                testData[0,k+2] = bone.next_joint.z
                k = k + 3 

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
    y = Scale(y, yMin, yMax, 0, constants.pygameWindowDepth)
    return (x, y)

def Handle_Frame(frame):
    hand = frame.hands[0]
    fingers = hand.fingers
    for finger in fingers:
        Handle_Finger(finger)
    
def Scale(value, sourceMin, sourceMax, targetMin, targetMax):
    sourceWidth = sourceMax-sourceMin
    if sourceWidth==0:
        sourceWidth = 1
    targetWidth = targetMax-targetMin
    sourceOffset = value-sourceMin

    return sourceOffset * targetWidth / sourceWidth + targetMin

def CenterData(data):
    x = data[0,::3]
    data[0,::3] -= np.mean(x)
    y = data[0,1::3]
    data[0,1::3] -= np.mean(y)
    z = data[0,2::3]
    data[0,2::3] -= np.mean(z)
    return data

pygameWindow = PYGAME_WINDOW()
x = constants.pygameWindowWidth/2
y = constants.pygameWindowDepth/2

# xMin, xMax, yMin, yMax = (-1000,1000,-1000,1000)
xMin, xMax, yMin, yMax = (0,0,0,0)

stretching = False

# Fastest way
def ReshapeData( sets, digits ):
    size = sets[0].shape[3]
    X = [ np.moveaxis(single_set, 3, 0) for single_set in sets]
    X = np.concatenate(X).reshape(len(digits)*size,-1)
    Y = [ np.array([single_digit]*size) for single_digit in digits]
    Y = np.concatenate(Y).flatten()
    return X, Y

while(True):
    pygameWindow.Prepare()

    stretching = False

    frame = controller.frame()
    if (len(frame.hands)>0):
        k = 0 
        Handle_Frame(frame)

        if use_standardization:
            testData = standardization.do(testData)
            X, Y = ReshapeData([testData], [0])
            #show.show_hand(testData[:,:,:,0], fname="Del2")
        else:
            testData = CenterData(testData)
            X = testData
        
        predictedClass = clf.Predict(X)
        print(predictedClass)

    # if stretching:
    #     #pygameWindow.Print("Stretching...")
    #     print("Stretching...")
    
    pygameWindow.Reveal()

