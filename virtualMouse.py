import cv2 as cv2
import time
import numpy as np
import math
import HandTracking as ht
import gestureControl as gc

"""Variable to use on the cam"""
controlMovenmt = gc.gestureControll()
WIDTH_CAM, HIGHT_CAM = (controlMovenmt.sizeScreen)

"""Setting camera"""
capCam = cv2.VideoCapture(0)
capCam.set(3, WIDTH_CAM)
capCam.set(4, HIGHT_CAM)

"""Setting hand recognition based on Mediapipe from Google"""

getGestureMovemnt = ht.handDetector(detectionCon=0.6)

while True:
    (success, img) = capCam.read()
    img = cv2.resize(img, (controlMovenmt.sizeScreen), interpolation=cv2.WINDOW_FULLSCREEN)
    img = cv2.flip(img, 1)
    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue
    
    img = getGestureMovemnt.findHands(img, draw=True)
    imgList = getGestureMovemnt.findPositionFingers(img, draw=False)
   

    if(len(imgList) != 0):
        x, y = imgList[8][1], imgList[8][2]
        #controlMovenmt.mouseMovement(x, y)
        print(f'distance between:\nindexTip{imgList[8]}\nmiddleTip{imgList[12]}')
        distanceIndexAndMiddleFinger = int(getGestureMovemnt.getDistance(imgList[8], imgList[12]))
        if(distanceIndexAndMiddleFinger <= 100):
            print('dedinhos juntos')
        if(distanceIndexAndMiddleFinger > 100):
            print('ta separado')
    #cv2.imshow("Gesture Recognition", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
