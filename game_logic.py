import pygame
import numpy as np
import math
import pickle

import pygame_resources
from lib import constants, pickle_database, standardization

db = pickle_database.Database()
programState = -1
pygame_screen = None
pygame_events = None
animation_screen = None
animation_screen_1 = None
gesture_screen = None
leapmotion_screen = None

leapmotion_controller = None
last_digit = 0
current_digit = 0
digit_correct_count = 0
success_icon_count = 0

img = pygame_resources.img
img_pos = pygame_resources.img_pos

testData = np.zeros((5, 4, 6), dtype='f')

# Classifier
clf = None


def Init():
    global animation_screen, animation_screen_1, leapmotion_screen, gesture_screen, clf
    animation_screen = pygame.Surface(
        (constants.pygameWindowWidth, constants.pygameWindowDepth),
        pygame.SRCALPHA, 32).convert_alpha()

    animation_screen_1 = pygame.Surface(
        (constants.pygameWindowWidth, constants.pygameWindowDepth),
        pygame.SRCALPHA, 32).convert_alpha()

    leapmotion_screen = pygame.Surface(
        (constants.pygameWindowWidth / 2, constants.pygameWindowDepth / 2),
        pygame.SRCALPHA, 32).convert_alpha()

    gesture_screen = pygame.Surface(
        (constants.pygameWindowWidth, constants.pygameWindowDepth),
        pygame.SRCALPHA, 32).convert_alpha()

    clf = pickle.load(open('mainData/classifier_with_standardization.p', 'rb'))


# Main entrance
def Game_Logic(screen, events, controller):
    global pygame_screen, pygame_events, leapmotion_controller
    pygame_screen = screen
    pygame_events = events
    leapmotion_controller = controller

    if programState == -1:
        Login()
    else:

        Main_Window()
        if programState == 0:  # the program is waiting to see the user's hand.
            GuideUserToUseHand()
        elif programState == 1:  # the user's hand is present but not centered.
            GuideToCenter()
        elif programState == 2:  # the user's hand is present and centered.
            LearnDigit()
        elif programState == 3:  # the user has correctly signed the current number.
            CorrectlySigned()

        DrawSuccessIcon()


# Login Window
def Login():
    global programState

    textsurface = pygame_resources.font["login_title"].render(
        "American Sign Language (ASL)", True, (0, 0, 0))
    pygame_screen.blit(textsurface, (170, 200))

    for digit in range(10):
        pygame_screen.blit(img["asl_small"][digit], (0, digit * 112))
        pygame_screen.blit(img["asl_small"][9 - digit],
                           (constants.pygameWindowWidth - 70, digit * 112))
    offset_x = 250
    offset_y = 500
    textsurface = pygame_resources.font["login_name"].render(
        "Please tell me your name: ___________", True, (0, 0, 0))
    pygame_screen.blit(textsurface, (offset_x, offset_y))

    ret = pygame_resources.inputs["username"].update(pygame_events)
    pygame_screen.blit(pygame_resources.inputs["username"].get_surface(),
                       (offset_x + 260, offset_y))
    if ret:  # Enter
        username = pygame_resources.inputs["username"].get_text()
        programState = 0
        db.login(username)
        db.inc('logins')
        generateNewDigit()


# Main Window
def Main_Window():
    pygame_screen.blit(img["back_img"], (0, 0))
    width = 1
    color = (124, 124, 124)
    pygame.draw.line(
        pygame_screen, color, (0, constants.pygameWindowDepth / 2),
        (constants.pygameWindowWidth, constants.pygameWindowDepth / 2), width)
    pygame.draw.line(
        pygame_screen, color, (constants.pygameWindowWidth / 2, 0),
        (constants.pygameWindowWidth / 2, constants.pygameWindowDepth), width)


def HandOverDevice():
    return (len(leapmotion_controller.frame().hands) > 0)


def DrawSensor():
    pygame_screen.blit(img["sensor"],
                       (img_pos["sensor_x"], img_pos["sensor_y"]))


# Leap motion Virtual Hands
def DrawBones():
    global testData
    testData = np.zeros((5, 4, 6), dtype='f')
    leapmotion_screen.fill(pygame.Color(0, 0, 0, 0))
    hand = leapmotion_controller.frame().hands[0]
    for finger in hand.fingers:
        for b in range(4):
            bone = finger.bone(b)
            base = bone.prev_joint
            tip = bone.next_joint
            testData[finger.type, bone.type, 0] = base.x
            testData[finger.type, bone.type, 1] = base.y
            testData[finger.type, bone.type, 2] = base.z
            testData[finger.type, bone.type, 3] = tip.x
            testData[finger.type, bone.type, 4] = tip.y
            testData[finger.type, bone.type, 5] = tip.z

    #testData = standardization.do(testData)
    if not math.isnan(testData[0, 0, 0]) and testData[0, 0, 0] != 0:
        for i in range(5):
            for j in range(4):
                pygame.draw.line(
                    leapmotion_screen, (0, 0, 0),
                    Handle_Vector_From_Leap(testData[i, j, 0],
                                            testData[i, j, 2]),
                    Handle_Vector_From_Leap(testData[i, j, 3],
                                            testData[i, j, 5]), 4 - j)


xMin, xMax, yMin, yMax = (-200, 200, -200, 200)


def Handle_Vector_From_Leap(x, y):
    global xMin, xMax, yMin, yMax
    if (x < xMin):
        xMin = x
    if (x > xMax):
        xMax = x
    if (y < yMin):
        yMin = y
    if (y > yMax):
        yMax = y
    x = Scale(x, xMin, xMax, 0, constants.divide_x)
    y = Scale(y, yMin, yMax, 0, constants.divide_y)
    return (x, y)


def Scale(value, sourceMin, sourceMax, targetMin, targetMax):
    sourceWidth = sourceMax - sourceMin
    if sourceWidth == 0:
        sourceWidth = 1
    targetWidth = targetMax - targetMin
    sourceOffset = value - sourceMin

    return sourceOffset * targetWidth / sourceWidth + targetMin


# Guiders
def GuideUserToUseHand():
    # Hand not present
    global programState
    for event in pygame_events:
        if event.type == constants.PY_ANIMATION_EVENT:
            offset = np.sin(pygame.time.get_ticks() / 400.) * 50
            animation_screen.fill(pygame.Color(0, 0, 0,
                                               0))  # clear animation screen
            animation_screen.blit(
                img["hand_2"], (img_pos["hand_x"] - offset, img_pos["hand_y"]))

    DrawSensor()
    pygame_screen.blit(animation_screen, (0, 0))
    if HandOverDevice():
        programState = 1


def HandInTheCenter():
    if not HandOverDevice():
        return False
    frame = leapmotion_controller.frame()
    p = frame.hands[0].fingers[0].bone(0).prev_joint
    return np.linalg.norm(np.array([p.x, p.y, p.z]) -
                          np.array([0, 300, 100])) < 200


def DrawVHand(other_img=None):
    frame = leapmotion_controller.frame()
    p = frame.hands[0].fingers[0].bone(0).prev_joint

    img_vhand_x = img_pos["sensor_x"] + p.x + 50
    img_vhand_y = img_pos["sensor_y"] - p.y / 2
    if other_img is None:
        pygame_screen.blit(img["hand_3"],
                           (img_pos["hand_x"], img_pos["hand_y"]))
        pygame_screen.blit(img["hand_2"], (img_vhand_x, img_vhand_y))
    else:
        pygame_screen.blit(other_img, (img_vhand_x, img_vhand_y))


def GuideToCenter():
    # Hand present but not in the center
    global programState
    DrawSensor()

    DrawBones()
    pygame_screen.blit(leapmotion_screen, (0, 0))

    if not HandOverDevice():
        programState = 0
        return

    if HandInTheCenter():
        DrawVHand(img["hand_g"])
        programState = 2
    else:
        DrawVHand()


# Digits
def generateNewDigit():
    global last_digit, current_digit, gesture_time_count
    digit = scaffolding_digit()
    if digit == last_digit:
        current_digit = np.random.randint(low=0, high=digit)
    else:
        current_digit = digit
    last_digit = current_digit
    gesture_time_count = 0
    SetProgressBar()


# Scaffolding
def scaffolding_digit():
    scaffolding_level = db.get("scaffolding_level")
    if scaffolding_level == None:
        db.set(1, "scaffolding_level")
        scaffolding_level = 1
    if scaffolding_level == 1:
        digit = db.get("scaffolding_level_1", "digit")
        if digit == None:
            db.set(1, "scaffolding_level_1", "digit")
            digit = 1
    else:
        digit = 9
    return digit


# Fastest way
def ReshapeData(sets, digits):
    size = sets[0].shape[3]
    X = [np.moveaxis(single_set, 3, 0) for single_set in sets]
    X = np.concatenate(X).reshape(len(digits) * size, -1)
    Y = [np.array([single_digit] * size) for single_digit in digits]
    Y = np.concatenate(Y).flatten()
    return X, Y


# Main Process: finally the users can start to learn digit.
def LearnDigit():
    # Hand in the Center
    global programState
    global testData
    global digit_correct_count, success_icon_count

    DrawLevel()
    DrawGesture()
    DrawProgressBar()

    if HandOverDevice():
        DrawBones()
        pygame_screen.blit(leapmotion_screen, (0, 0))

        testData = standardization.do(testData)
        X, Y = ReshapeData([testData], [0])

        predictedClass = clf.Predict(X)
        textsurface = pygame_resources.font["digit_large"].render(
            "%d" % predictedClass[0], True, (230, 230, 230))
        pygame_screen.blit(textsurface,
                           (constants.divide_x + 10, constants.divide_y + 10))
        if predictedClass[0] == current_digit:
            textsurface = pygame_resources.font["digit_large"].render(
                "%d" % current_digit, True, (81, 250, 10))
            pygame_screen.blit(
                textsurface, (img_pos["asl_digit_x"], img_pos["asl_digit_y"]))

            digit_correct_count += 1
        else:
            textsurface = pygame_resources.font["digit_large"].render(
                "%d" % current_digit, True, (0, 0, 0))
            pygame_screen.blit(textsurface,
                            (img_pos["asl_digit_x"], img_pos["asl_digit_y"]))
            digit_correct_count = 0

    if digit_correct_count > 30:
        digit_correct_count = 0
        programState = 3
        success_icon_count = 30
        scaffolding_success()

    if not HandInTheCenter():
        programState = 1

gesture_time_count = 0
def DrawGesture():
    global gesture_time_count
    gesture_screen.fill(pygame.Color(0,0,0,0))
    if db.get("scaffolding_level")==2:
        # blink the hints
        s = db.get("scaffolding_level_2", "success")
        # success [0,100]
        gesture_time_count += 1
        duration = 60
        if (gesture_time_count%duration>min(s*2,duration-2)):
            gesture_screen.blit(img["asl"][current_digit],
                        (img_pos["asl_x"], img_pos["asl_y"]))

    elif db.get("scaffolding_level")==1:
        gesture_screen.blit(img["asl"][current_digit],
                        (img_pos["asl_x"], img_pos["asl_y"]))

    pygame_screen.blit(gesture_screen, (0,0))


def scaffolding_success():
    scaffolding_level = db.get("scaffolding_level")
    if scaffolding_level == 1:
        d = db.get("scaffolding_level_1", "digit")
        if current_digit == d:
            db.inc("scaffolding_level_1", "success")
            success = db.get("scaffolding_level_1", "success")
            if success >= constants.success_needed_for_unlock_new_digit:
                if d == 9:
                    db.inc("scaffolding_level")
                    db.set(0, "scaffolding_level_2", "success")
                else:
                    db.inc("scaffolding_level_1", "digit")
                    db.set(0, "scaffolding_level_1", "success")
    if scaffolding_level == 2:
        db.inc("scaffolding_level_2", "success")
        if db.get("scaffolding_level_2", "success")>50:
            db.inc("scaffolding_level")
    if scaffolding_level == 3:
        db.inc("scaffolding_level_3", "success")


def CorrectlySigned():
    global programState
    programState = 2
    generateNewDigit()


def DrawSuccessIcon():
    global success_icon_count
    for event in pygame_events:
        if event.type==constants.PY_ANIMATION_EVENT:
            animation_screen_1.fill(pygame.Color(0, 0, 0, 0))  # clear animation screen
            if success_icon_count > 0:
                animation_screen_1.blit(
                    img["success"], (img_pos["success_x"] - success_icon_count * 4,
                                    img_pos["success_y"]))
                success_icon_count -= 1
    pygame_screen.blit(animation_screen_1, (0, 0))

progress_bar_count = 0
def SetProgressBar():
    global progress_bar_count
    progress_bar_count = constants.pygameWindowWidth - constants.divide_x

def DrawProgressBar():
    global progress_bar_count
    if progress_bar_count>0:
        if db.get("scaffolding_level_3", "success") is not None:
            progress_bar_count-= min(db.get("scaffolding_level_3", "success"), 10)
            
            pygame.draw.rect(pygame_screen, (41, 100, 10), 
                pygame.Rect(constants.pygameWindowWidth-progress_bar_count,constants.pygameWindowDepth-15,constants.pygameWindowWidth, constants.pygameWindowDepth-2))

def DrawLevel():
    level = db.get("scaffolding_level")
    textsurface = pygame_resources.font["login_title"].render(
        "Level %d"%level, True, (0, 0, 0))
    x = (constants.pygameWindowWidth + constants.divide_x - textsurface.get_width()) / 2
    y = (constants.divide_y - textsurface.get_height()) / 2
    pygame_screen.blit(textsurface, (x, y))

if __name__ == "__main__":
    import main_2
