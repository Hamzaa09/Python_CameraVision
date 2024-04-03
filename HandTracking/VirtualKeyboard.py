import cv2 
import time 
import HandTrackingModule as htm
import pyautogui

cap = cv2.VideoCapture(0)
detector = htm.handDetector(maxHands=1)


delayer = 0

# Text To Display
text = ''

while True:
    success, img = cap.read() 
    img = cv2.flip(img,1)
    img = cv2.resize(img, (820, 600))
    img = detector.findHands(img)
    lmlist = detector.findPosition(img)
    fingers = detector.fingersCounter()

    if delayer>100:
        delayer=0

    # First Line
    initialPoints_1 = [20,50]
    finalPoints_1 = [initialPoints_1[0]+80,initialPoints_1[1]+80]
    alphabetsList_1 = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']

    for i in range(10):
        
        # Key Pressing
        color = (220,100,255)
        if lmlist:
            if fingers[1]:
                if lmlist[8][1]>initialPoints_1[0] and lmlist[8][1]<finalPoints_1[0] and lmlist[8][2]>initialPoints_1[1] and lmlist[8][2]<finalPoints_1[1]: 
                    color = (225,0,255)
                    if fingers[2] and delayer % 7 == 0:
                        text += alphabetsList_1[i]

        # Drawing 
        cv2.rectangle(img,initialPoints_1,finalPoints_1,color,cv2.FILLED)
        cv2.putText(img, f'{alphabetsList_1[i]}',(initialPoints_1[0]+22,initialPoints_1[1]+45),cv2.FONT_HERSHEY_COMPLEX,1,(0),2)
        initialPoints_1 = [finalPoints_1[0]+10,initialPoints_1[1]]
        finalPoints_1 = [finalPoints_1[0]+80,finalPoints_1[1]]


    # Second Line
    initialPoints_2 = [50,150]
    finalPoints_2 = [initialPoints_2[0]+80,initialPoints_2[1]+80]
    alphabetsList_2 = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L']

    for i in range(9):
        
        # Key Pressing
        color = (220,100,255)
        if lmlist:
            if fingers[1]:
                if lmlist[8][1]>initialPoints_2[0] and lmlist[8][1]<finalPoints_2[0] and lmlist[8][2]>initialPoints_2[1] and lmlist[8][2]<finalPoints_2[1]: 
                    color = (225,0,255)
                    if fingers[2] and delayer % 7 == 0:
                        text += alphabetsList_2[i]

        # Drawing 
        cv2.rectangle(img,initialPoints_2,finalPoints_2,color,cv2.FILLED)
        cv2.putText(img, f'{alphabetsList_2[i]}',(initialPoints_2[0]+22,initialPoints_2[1]+45),cv2.FONT_HERSHEY_COMPLEX,1,(0),2)
        initialPoints_2 = [finalPoints_2[0]+10,initialPoints_2[1]]
        finalPoints_2 = [finalPoints_2[0]+80,finalPoints_2[1]]


    # Third Line
    initialPoints_3 = [100,250]
    finalPoints_3 = [initialPoints_3[0]+80,initialPoints_3[1]+80]
    alphabetsList_3 = ['Z', 'X', 'C', 'V', 'B', 'N', 'M']

    for i in range(7):
        
        # Key Pressing
        color = (220,100,255)
        if lmlist:
            if fingers[1]:
                if lmlist[8][1]>initialPoints_3[0] and lmlist[8][1]<finalPoints_3[0] and lmlist[8][2]>initialPoints_3[1] and lmlist[8][2]<finalPoints_3[1]: 
                    color = (225,0,255)
                    if fingers[2] and delayer % 7 == 0:
                        text += alphabetsList_3[i]

        # Drawing         
        cv2.rectangle(img,initialPoints_3,finalPoints_3,color,cv2.FILLED)
        cv2.putText(img, f'{alphabetsList_3[i]}',(initialPoints_3[0]+22,initialPoints_3[1]+45),cv2.FONT_HERSHEY_COMPLEX,1,(0),2)
        initialPoints_3 = [finalPoints_3[0]+10,initialPoints_3[1]]
        finalPoints_3 = [finalPoints_3[0]+80,finalPoints_3[1]]


    cv2.rectangle(img, (50,400), (800,500),(220,100,255),cv2.FILLED)
    cv2.putText(img, f'{text}',(80,450),cv2.FONT_HERSHEY_COMPLEX,1,(0),2)

    delayer+=1

    cv2.imshow("Virual keyboard",img)
    cv2.waitKey(1)