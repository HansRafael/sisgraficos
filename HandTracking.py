"""
Hand Tracking Module
By: Murtaza Hassan
Youtube: http://www.youtube.com/c/MurtazasWorkshopRoboticsandAI
Website: https://www.computervision.zone
"""

import cv2
import mediapipe as mp
import time
import math

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,self.mpHands.HAND_CONNECTIONS)
        return img

    def findPositionFingers(self, img, draw=True):
        xPositionList = []
        yPositionList = []
        bbox = []
        self.fingersList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[0] 
        
            for id, fingerPosition in enumerate(myHand.landmark):
                hightImage, widthImage, _ = img.shape
                
                xScreen = int(fingerPosition.x * widthImage)
                yScreen = int(fingerPosition.y * hightImage)
                xPositionList.append(xScreen)
                yPositionList.append(yScreen)

                self.fingersList.append([id, xScreen,yScreen])
                if draw:
                    cv2.circle(img, (xScreen, yScreen), 5, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(xPositionList), max(xPositionList)
            ymin, ymax = min(yPositionList), max(yPositionList)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                    (bbox[2] + 20, bbox[3] + 20), (0, 255, 0), 2)

        return self.fingersList

    def getDistance(self, indexFingerTip, middleFingerTip):
        xIndex, yIndex = indexFingerTip[1], indexFingerTip[2]
        xMiddle, yMiddle = middleFingerTip[1], middleFingerTip[2]
        
        return(math.dist([xIndex,yIndex], [xMiddle, yMiddle]))


