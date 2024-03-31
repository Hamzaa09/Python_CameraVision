import cv2
import time,os
import pyautogui
import numpy as np
import mediapipe as mp
import HandTrackingModule as htm


folder = 'Hand Tracking\images'
list = os.listdir(folder)
oslist = []
for imPath in list:
    images = cv2.imread(f'{folder}/{imPath}')
    oslist.append(images)
image = oslist[1]


cap = cv2.VideoCapture(0)
detector = htm.handDetector()


color = (0,255,0)
thickness = 5
x,y = 0,0


imgCanvas = np.zeros((480,640,3),np.uint8)
while True:
    success, img = cap.read()
    img = cv2.flip(img,1)

    img = detector.findHands(img)
    lmlist = detector.findPosition(img)
    fingers = detector.fingersCounter()
    
    if lmlist:
        x1,y1 = lmlist[8][1:]
        x2,y2 = lmlist[12][1:]

        # Drawing Mode
        if fingers[1] and fingers[2]==0:
            cv2.circle(img, (x1,y1), 7, color, cv2.FILLED)
            if x==0 and y==0:
                x,y = x1,y1
            if color==0:
                cv2.line(imgCanvas, (x,y),(x1,y1), color, 30)

            cv2.line(imgCanvas, (x,y),(x1,y1), color, thickness)
            x,y = x1,y1

        # Selection Mode
        if fingers[1] and fingers[2]:
            x,y = 0,0
            if lmlist[12][1]>0 and lmlist[12][1]<140 and lmlist[12][2]<50:
                image = oslist[1]
                color=(0,255,0)
            if lmlist[12][1]>140 and lmlist[12][1]<240 and lmlist[12][2]<50:
                image = oslist[2]
                color=(0,0,255)
            if lmlist[12][1]>240 and lmlist[12][1]<340 and lmlist[12][2]<50:
                image = oslist[3]
                color=(255,0,0)
            if lmlist[12][1]>340 and lmlist[12][1]<440 and lmlist[12][2]<50:
                image = oslist[4]
                color=(0,255,255)
            if lmlist[12][1]>440 and lmlist[12][1]<540 and lmlist[12][2]<50:
                image = oslist[5]
                color=(255,0,255)
            if lmlist[12][1]>540 and lmlist[12][1]<640 and lmlist[12][2]<50:
                image = oslist[6]
                color=0
                
            cv2.rectangle(img, (x2,y2),(x2-20,y2+20),color,cv2.FILLED)

    # image conversion
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray,50,255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # Final Display
    img[0:50, 0:640] = image
    cv2.imshow("Virtual Painter",img)
    # cv2.imshow("Vir/tual Painter CAnvas",imgCanvas)
    cv2.waitKey(1)