import cv2 as cv2
import time
import numpy as np
import math
import HandTracking as ht
import gestureControl as gc

"""Variable to use on the cam"""
controlMovement = gc.gestureControll()
WIDTH_SCREEN, HIGHT_SCREEN = (controlMovement.sizeScreen)
wCam, hCam = 640, 480
FRAME_RATE = 100
TWO_FINGERSs = [0,1,1,0,0]
TWO_FINGERS = [1,1,1,0,0]
THREE_FINGERS = [1,1,1,1,0]
FOUR_FINGERS = [1,1,1,1,1]
FINGER = 12
pTime = 0
"""Setting camera"""
capCam = cv2.VideoCapture(0)
capCam.set(3, wCam)
capCam.set(4, hCam)

"""Setting hand recognition based on Mediapipe from Google"""
handTracking = ht.handDetector(detectionCon=0.6)
lastPositionY = 0
while True:
    (success, img) = capCam.read()
    if not success:
        print("Ignoring empty camera frame.")
        print(img)
        # If loading a video, use 'break' instead of 'continue'.
        continue
    
    img = cv2.flip(img, 1)
    cv2.rectangle(img, (FRAME_RATE, FRAME_RATE), (wCam - FRAME_RATE , hCam - FRAME_RATE ), (255, 0, 255), 2)
    cv2.putText(img, f'Stay on the rectangle', (600, 440), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 3)
    img = handTracking.findHands(img, draw=True)
    imgList, handBox = handTracking.findPositionFingers(img, draw=True)
   
    up = False
    down = False
    if(len(imgList) != 0):
        xCenter, yCenter = handTracking.getCenterRectancle(handBox)
        if(lastPositionY > yCenter):
            up = True
            lastPositionY = yCenter
        if(lastPositionY < yCenter):
            down = True
            lastPositionY = yCenter

        fingerUp = handTracking.fingersUp()

        if(fingerUp == THREE_FINGERS):
            if(up):
                controlMovement.scrollWheel(5, 1)
                up = False
            elif(down):
                controlMovement.scrollWheel(5, -1)
                down=False

        if(fingerUp == FOUR_FINGERS):
            print('4 dedoss')
        
        if(fingerUp == TWO_FINGERS or fingerUp == TWO_FINGERSs):
            x, y = imgList[FINGER][1], imgList[FINGER][2]
            x3 = np.interp(x, (FRAME_RATE, wCam - FRAME_RATE), (0, WIDTH_SCREEN))
            y3 = np.interp(y, (FRAME_RATE, hCam - FRAME_RATE), (0, HIGHT_SCREEN))
            controlMovement.mousemove(x3,y3)
            if(fingerUp[0] == 1):
                controlMovement.mouseclick(x3,y3)

        distanceIndexAndMiddleFinger = handTracking.getDistance(imgList[FINGER], imgList[8])
        #print(f'distance between indexTip and middleTip: {distanceIndexAndMiddleFinger}')

    # Frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 2)
    cv2.imshow("Gesture Recognition", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
