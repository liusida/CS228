import numpy as np
import pickle

import sys
sys.path.insert(0, '../LeapSDK/lib')
sys.path.insert(0, '../LeapSDK/lib/x86')
import Leap

from lib.knn import KNN
from lib.pygameWindow import PYGAME_WINDOW
from lib import constants, standardization, show, pickle_database


db = pickle_database.Database()

do_classifier = True
divide_x = constants.pygameWindowWidth / 2
divide_y = constants.pygameWindowDepth / 2

clf = pickle.load( open('mainData/classifier_with_standardization.p','rb') )
testData = np.zeros((5,4,6),dtype='f')

controller = Leap.Controller()

def Handle_Finger(finger):
    global k, testData
    for b in range(4):
        bone = finger.bone(b)
        Handle_Bone(bone)
        testData[finger.type, bone.type, 0] = bone.prev_joint.x
        testData[finger.type, bone.type, 1] = bone.prev_joint.y
        testData[finger.type, bone.type, 2] = bone.prev_joint.z
        testData[finger.type, bone.type, 3] = bone.next_joint.x
        testData[finger.type, bone.type, 4] = bone.next_joint.y
        testData[finger.type, bone.type, 5] = bone.next_joint.z

def Handle_Bone(bone):
    global pygameWindow
    base = bone.prev_joint
    tip = bone.next_joint
    pygameWindow.Draw_Black_Line(Handle_Vector_From_Leap(base), Handle_Vector_From_Leap(tip), 4-bone.type)

def Handle_Vector_From_Leap(v):
    global xMin, xMax, yMin, yMax
    x=v.x
    y=v.z
    if (x<xMin):
        xMin = x
    if (x>xMax):
        xMax = x
    if (y<yMin):
        yMin = y
    if (y>yMax):
        yMax = y
    x = Scale(x, xMin, xMax, 0, divide_x)
    y = Scale(y, yMin, yMax, 0, divide_y)
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
#x = constants.pygameWindowWidth/2
#y = constants.pygameWindowDepth/2

# xMin, xMax, yMin, yMax = (-1000,1000,-1000,1000)
xMin, xMax, yMin, yMax = (0,0,0,0)

# Fastest way
def ReshapeData( sets, digits ):
    size = sets[0].shape[3]
    X = [ np.moveaxis(single_set, 3, 0) for single_set in sets]
    X = np.concatenate(X).reshape(len(digits)*size,-1)
    Y = [ np.array([single_digit]*size) for single_digit in digits]
    Y = np.concatenate(Y).flatten()
    return X, Y


img_hand_2 = pygameWindow.LoadImg('images/vhand_2.png')
img_hand_3 = pygameWindow.LoadImg('images/vhand_3.png')
img_hand_g = pygameWindow.LoadImg('images/vhand_g.png')
img_hand_x = divide_x + (constants.pygameWindowWidth-divide_x)/2 - img_hand_2.get_width()/2
img_hand_y = divide_y/2 - img_hand_2.get_height()/2 -80
img_sensor = pygameWindow.LoadImg('images/sensor_t.png')
img_sensor_x = divide_x + (constants.pygameWindowWidth-divide_x)/2 - img_sensor.get_width()/2
img_sensor_y = divide_y/2 - img_sensor.get_height()/2 + 80
green_x = constants.pygameWindowWidth - 40
green_y = 60
green_size = 30

asl_small = []
asl = []
for i in range(10):
    asl.append(pygameWindow.LoadImg('images/ASL/%d.png'%i, (140,224)))
    asl_small.append(pygameWindow.LoadImg('images/ASL/%d.png'%i))
asl_x = divide_x + (constants.pygameWindowWidth-divide_x)/2 - asl[0].get_width()/2
asl_y = divide_y + (constants.pygameWindowDepth-divide_y)/2 - asl[0].get_height()/2
programState = -1
def DrawSensor():
    pygameWindow.DrawImg( img_sensor, (img_sensor_x, img_sensor_y) )

asl_digit_x = divide_x + (constants.pygameWindowWidth-divide_x)/2 - 20
asl_digit_y = divide_y + 50

img_success = pygameWindow.LoadImg('images/success.png')
img_success_x = constants.pygameWindowWidth
img_success_y = 5

time_1 = 0
def DrawImageToHelpUserPutTheirHandOverTheDevice():
    global time_1
    time_1 += 1
    offset = time_1%500/5
    if offset>50:
        offset = 100-offset
    pygameWindow.DrawImg( img_hand_2, (img_hand_x+25-offset, img_hand_y))
    DrawSensor()

time_3 = 0
def DrawVHand(img=None):
    global time_3
    time_3 += 1
    frame = controller.frame()
    p = frame.hands[0].fingers[0].bone(0).prev_joint

    img_vhand_x = img_sensor_x + p.x + 50

    img_vhand_y = img_sensor_y - p.y / 2
    if img is None:
        img=img_hand_2
        pygameWindow.DrawImg( img_hand_3, (img_hand_x, img_hand_y))
        pygameWindow.DrawImg( img_hand_2, (img_vhand_x, img_vhand_y) )
    else:
        pygameWindow.DrawImg( img, (img_vhand_x, img_vhand_y) )
        
    

def HandOverDevice():
    frame = controller.frame()
    return len(frame.hands)>0

def HandInTheCenter():
    frame = controller.frame()
    p = frame.hands[0].fingers[0].bone(0).prev_joint
    #print(p.x, p.y, p.z)
    scope = 200
    offset_y = 300
    offset_z = 100
    if p.x < -scope:
        return 1 #too left
    if p.x > scope:
        return 2 #too right
    if p.y < -scope+offset_y:
        return 3 #too close
    if p.y > scope+offset_y:
        return 4 #too far
    if p.z <-scope+offset_z:
        return 5 # too inside
    if p.z > scope+offset_z:
        return 6 # too outside
    return 0

def HandleState0(): 
    # Hand not present
    global programState
    DrawImageToHelpUserPutTheirHandOverTheDevice()
    if HandOverDevice():
        programState=1

time_2 = 0
def HandleState1():
    # Hand present but not in the center
    global programState
    global time_2
    global k
    DrawSensor()
    frame = controller.frame()
    k=0
    Handle_Frame(frame)

    if not HandOverDevice():
        programState=0
    hand_position = HandInTheCenter()
    if hand_position==0:
        time_2 += 1
        DrawVHand(img_hand_g)
    else:
        DrawVHand()

    if time_2 > 100:
        time_2 = 0
        programState=2
        
time_4 = 0
def HandleState2():
    # Hand in the Center
    global programState
    global testData, k
    global time_4
    
    pygameWindow.DrawImg( asl[digit], (asl_x, asl_y) )
    pygameWindow.Text("%d"%digit, size=60, position=(asl_digit_x, asl_digit_y))
    frame = controller.frame()
    if (len(frame.hands)>0):
        k = 0 
        Handle_Frame(frame)

        if do_classifier:
            testData = standardization.do(testData)
            X, Y = ReshapeData([testData], [0])
            
            predictedClass = clf.Predict(X)
            #print(predictedClass[0], digit)
            pygameWindow.Text("%d"%predictedClass[0], color=(230,230,230), size=60, position=(divide_x+10, divide_y+10))
            pygameWindow.Text("This digit has been presented %d times."%digit_presented_times, size=20, position=(divide_x+20,constants.pygameWindowDepth-40))
            if predictedClass[0] == digit:
                pygameWindow.Text("%d"%digit, color=(81,250,10), size=60, position=(asl_digit_x, asl_digit_y))
                time_4 += 1
            else:
                time_4 = 0
    if time_4 > 20:
        time_4 = 0
        programState=3

    if HandInTheCenter()>0:
        programState=1

digit_presented_times = 0
def HandleState3():
    global time_success, programState
    time_success = 100
    programState=2
    generateNewDigit()

def generateNewDigit():
    global digit, digit_presented_times
    digit = np.random.randint(low=0, high=10)
    db.inc('attempted_%d'%digit)
    digit_presented_times = db.get('attempted_%d'%digit)


time_success = 0
def Success():
    if time_success>0:
        pygameWindow.DrawImg(img_success, (img_success_x-time_success, img_success_y))
        time_success -= 1


def Login(events):
    global programState
    pygameWindow.Text("American Sign Language (ASL)", size=40, position=(170,200))
    for digit in range(10):
        pygameWindow.DrawImg( asl_small[digit], (0, digit*112) )
        pygameWindow.DrawImg( asl_small[9-digit], (constants.pygameWindowWidth-70, digit*112) )
            
    offset_x = 250
    offset_y = 500
    pygameWindow.Text("Please tell me your name: ___________", position=(offset_x, offset_y), size=20)
    ret = pygameWindow.Input(events, position=(offset_x+260, offset_y))
    if ret: # Enter
        username = pygameWindow.textinput.get_text()
        programState = 0
        db.login(username)
        db.inc('logins')
        generateNewDigit()

while(True):
    events = pygameWindow.Prepare()
    if events == -1:
        break

    if programState == -1:
        Login(events)
    else:

        pygameWindow.SeparateWindows()

        if programState == 0: # the program is waiting to see the user's hand. 
            HandleState0() 
        elif programState == 1: # the user's hand is present but not centered. 
            HandleState1()
        elif programState == 2: # the user's hand is present and centered. 
            HandleState2()
        elif programState == 3: # the user has correctly signed the current number.
            HandleState3()

    pygameWindow.Reveal()
