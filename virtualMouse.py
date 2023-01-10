import cv2 as cv2
import time
import numpy as np
import math
import HandTracking as ht

"""Variable to use on the cam"""
WIDTH_CAM, HIGHT_CAM = 640, 480

"""Setting camera"""
capCam = cv2.VideoCapture(0)
capCam.set(3, WIDTH_CAM)
capCam.set(4, HIGHT_CAM)

"""Setting hand recognition based on Mediapipe from Google"""

getGestureMovemnt = ht.handDetector(detectionCon=0.7)

while True:
    (success, img) = capCam.read()
    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue
    
    img = getGestureMovemnt.findHands(img)


    cv2.imshow("Gesture Recognition", cv2.flip(img, 1))
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
