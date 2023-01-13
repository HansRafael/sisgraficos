import cv2 as cv2
import time
import numpy as np
import math
import HandTracking as ht
import gestureControl as gc

"""Variable to use on the cam"""
controlMovement = gc.gestureControll()
WIDTH_CAM, HIGHT_CAM = (controlMovement.sizeScreen)
TWO_FINGERSs = [0,1,1,0,0]
TWO_FINGERS = [1,1,1,0,0]
THREE_FINGERS = [1,1,1,1,0]
FOUR_FINGERS = [1,1,1,1,1]
FINGER = 12
pTime = 0
"""Setting camera"""
capCam = cv2.VideoCapture(0)
capCam.set(3, WIDTH_CAM)
capCam.set(4, HIGHT_CAM)

"""Setting hand recognition based on Mediapipe from Google"""
handTracking = ht.handDetector(detectionCon=0.6)

while True:
    (success, img) = capCam.read()
    if not success:
        print("Ignoring empty camera frame.")
        print(img)
        # If loading a video, use 'break' instead of 'continue'.
        continue
    
    img = cv2.resize(img, (controlMovement.sizeScreen), interpolation=cv2.WINDOW_FULLSCREEN)
    img = cv2.flip(img, 1)
    img = handTracking.findHands(img, draw=True)
    imgList, handBox = handTracking.findPositionFingers(img, draw=True)
   

    if(len(imgList) != 0):
        area = handTracking.getAreaBox(handBox)
        cv2.putText(img, f'AREA HAND BOX: {area}', (1000, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
        fingerUp = handTracking.fingersUp()

        if ( 500 < area < 2000):
            print(fingerUp)
            if(fingerUp == THREE_FINGERS):
                print('3 dedoss')

            if(fingerUp == FOUR_FINGERS):
                print('4 dedoss')
            
            if(fingerUp == TWO_FINGERS or fingerUp == TWO_FINGERSs):
                x, y = imgList[FINGER][1], imgList[FINGER][2]
                controlMovement.mousemove(x,y)
                if(fingerUp[0] == 1):
                    controlMovement.mouseclick(x,y)

            distanceIndexAndMiddleFinger = handTracking.getDistance(imgList[FINGER], imgList[8])
            #print(f'distance between indexTip and middleTip: {distanceIndexAndMiddleFinger}')

        else:
            cv2.putText(img, f'OUT OF AREA! STAY BETWEEN 500 AND 2000!:', (250, 800), cv2.FONT_HERSHEY_COMPLEX, 1, (125, 125, 255), 3)
    
    # Frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)
    cv2.imshow("Gesture Recognition", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
