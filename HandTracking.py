import cv2
import mediapipe as mp

class HandDetector():
    def __init__(self, mode=False, maxHands=1, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, 
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #COLOR_BGR2RGB returns image in RGB format, which was initially in BGR format as read by cv2. imread()
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
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[0] 
        
            for id, fingerPosition in enumerate(myHand.landmark):
                hightImage, widthImage, _ = img.shape
                
                xScreen = int(fingerPosition.x * widthImage)
                yScreen = int(fingerPosition.y * hightImage)
                
                xPositionList.append(xScreen)
                yPositionList.append(yScreen)

                xmin, xmax = min(xPositionList), max(xPositionList)
                ymin, ymax = min(yPositionList), max(yPositionList)
                bbox = xmin, ymin, xmax, ymax
        

                self.lmList.append([id, xScreen,yScreen])
            if draw:
                cv2.rectangle(img, (bbox[0] - 15, bbox[1] - 15), (bbox[2] + 15, bbox[3] + 15), (0, 255, 0), 2)
        return self.lmList, bbox

    def fingersUp(self):
        fingers = []
        # Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 Fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers


