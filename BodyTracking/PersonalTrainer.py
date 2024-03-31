import time
import cv2
import sys
import numpy as np
import mediapipe as mp 
import BodyTrackingModule as btm
sys.path.insert(1,'C:\\Users\\LUCKY COMPUTER\\OneDrive\\Python_Cameralook\\Hand Tracking')
import HandTrackingModule as htm

# Menu Function
def menu(img,lmlist2,fingers):

    # Options Diagram
    cv2.rectangle(img ,(0,0), (210,90),(255,0,255),1)
    cv2.putText(img, ' PushUps ', (20,50), 2 , cv2.FONT_HERSHEY_PLAIN , (255,255,255),3)
    cv2.rectangle(img ,(215,0), (425,90),(255,0,255),1)
    cv2.putText(img, ' Sit Ups ', (230,50), 2 , cv2.FONT_HERSHEY_PLAIN , (255,255,255),3)
    cv2.rectangle(img ,(430,0), (638,90),(255,0,255),1)
    cv2.putText(img, ' Dumbbells ', (440,50), 2 , cv2.FONT_HERSHEY_PLAIN , (255,255,255),3)

    # Selections
    if lmlist2:
        if fingers[1] and fingers[2]:
            if lmlist2[12][1]>0 and lmlist2[12][1]<210 and lmlist2[12][2]<90:
                return 1
            elif lmlist2[12][1]>215 and lmlist2[12][1]<425 and lmlist2[12][2]<90:
                return 2
            elif lmlist2[12][1]>430 and lmlist2[12][1]<638 and lmlist2[12][2]<90:
                return 3
            else:
                return 0

cap = cv2.VideoCapture(0)

detector = btm.bodyTracking()
detector2 = htm.handDetector(maxHands=1)

a1,a2,count,dir = 0,0,0,0
menu_disp=1

while True:
    # For Body
    success, img = cap.read()
    img = cv2.flip(img,1)
    img = detector.findPose(img,False)
    lmlist = detector.getPositions(img)

    # For Hand
    img = detector2.findHands(img,False)
    lmlist2 = detector2.findPosition(img)
    fingers = detector2.fingersCounter()

    # Calling menu Function
    if menu_disp:
        check = menu(img,lmlist2,fingers)
        
    # Counter Code
    if lmlist:
        landmrksList=[11,13,15]

        if check==1:
            landmrksList[1],landmrksList[2]=13,15
            a1,a2=70,170
            cv2.putText(img,'Pushups',(440,50), 2 , cv2.FONT_HERSHEY_PLAIN , (255,0,255),2)

        elif check==2:
            landmrksList[1],landmrksList[2]=23,25
            a1,a2=40,150
            cv2.putText(img,'SitUps',(440,50), 2 , cv2.FONT_HERSHEY_PLAIN , (255,0,255),2)

        elif check==3:
            landmrksList[1],landmrksList[2]=13,15
            a1,a2=40,150
            cv2.putText(img,'DumbBells',(440,50), 2 , cv2.FONT_HERSHEY_PLAIN , (255,0,255),2)
        else:
            landmrksList[1],landmrksList[2]=0,0
            a1,a2=0,0

        if lmlist[landmrksList[0]] and lmlist[landmrksList[1]] and lmlist[landmrksList[2]]:
            if a1 and a2:
                menu_disp=0
                h, w, c = img.shape
                angle = detector.getAngle(img, landmrksList[0], landmrksList[1], landmrksList[2])
                bar = np.interp(angle,[a1,a2],[100,400])
                percentage = np.interp(angle,[a1,a2],[100,0])

                cv2.rectangle(img, (100,400), (50,100), (255,0,255), 2)
                cv2.rectangle(img, (100,400), (50,int(bar)), (255,0,255), cv2.FILLED)
                cv2.putText(img, f'{int(percentage)}%', (50,80), 2 , cv2.FONT_HERSHEY_PLAIN , (255,0,255),2)
                
                if percentage == 100:
                    cv2.rectangle(img, (100,400), (50,100), (255,255,255), cv2.FILLED)
                    if dir == 0:
                        count+=0.5
                        dir = 1
                if percentage == 0:
                    cv2.rectangle(img, (100,400), (50,100), (255,255,255),2)
                    if dir == 1:
                        count+=0.5
                        dir = 0

                # Angle display
                cv2.putText(img, f'{int(angle)}', (lmlist[landmrksList[1]][1]+50,lmlist[landmrksList[1]][2]), 2 , cv2.FONT_HERSHEY_PLAIN , (255,0,255),2)

                # Counter 
                cv2.rectangle(img, (480,60), (580,140), (255,255,255), cv2.FILLED)
                cv2.putText(img, f'{int(count)}', (520,110), 2 , cv2.FONT_HERSHEY_PLAIN , (255,0,255),2)
                
                # Menu Calling
                cv2.rectangle(img, (500,400), (640,480), (255,255,255), cv2.FILLED)
                cv2.putText(img, 'Exit', (540,450), 2 , cv2.FONT_HERSHEY_PLAIN , (255,0,255),2)
                if lmlist2:
                    if lmlist2[12][1]>500 and lmlist2[12][2]>400: 
                        menu_disp=1
                        check,count = 0,0
    
    cv2.imshow("Ai Trainer", img)
    cv2.waitKey(1)