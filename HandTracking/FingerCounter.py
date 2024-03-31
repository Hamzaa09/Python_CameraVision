import cv2
import time
import os
import HandTrackingModule as htm

cap  = cv2.VideoCapture(0)
detector = htm.handDetector(maxHands=1)

tipList = [8,12,16,20]

pTime = 0
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img)

    if lmlist:
        fingerUpList = []
        if lmlist[4][1] > lmlist[2][1]:
            fingerUpList.append(1)
        else:
            fingerUpList.append(0)

        for id in range(4):
            if lmlist[tipList[id]][2] < lmlist[tipList[id]-2][2]:
                fingerUpList.append(1)
            else:
                fingerUpList.append(0)

        cv2.rectangle(img, (0,400),(80,600), (0), cv2.FILLED)
        cv2.putText(img, f'{fingerUpList.count(1)}', (30,450), cv2.FONT_HERSHEY_PLAIN , 2, (255), 2)
    


    cTime = time.time()
    fps = int(1/(cTime-pTime))
    pTime = cTime

    cv2.putText(img, f'FPS:{fps}', (20,40), cv2.FONT_HERSHEY_PLAIN , 2, (0), 2)
    cv2.imshow("Finger Counter", img)
    cv2.waitKey(1)
