# 640x480

# volume control -
# right click -
# left skip -
# right skip -
# mouse wheel up -
# mouse wheel down -
import time
import cv2
import numpy as np
import HandTrackingModule as htm
import math
import mouse, pyautogui
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

volume = interface.QueryInterface(IAudioEndpointVolume)

volume.GetVolumeRange()

cap = cv2.VideoCapture(0)
detector = htm.handDetector(maxHands=1)


cTime = 0
pTime = 0
volBar = 400
volPer = 0
while True:
    success,img = cap.read()
    img = cv2.flip(img,1)
    img = detector.findHands(img)
    lmlist = detector.findPosition(img)
    fingers = detector.fingersCounter()


    if lmlist:
        # Mouse Control
        if {fingers[i] for i in [1,2]} == {1} and {fingers[i] for i in [0,3,4]} == {0}:
            x1,y1 = lmlist[8][1],lmlist[8][2]
            x2,y2 = lmlist[12][1],lmlist[12][2]
            x = np.interp(x2, [100,540],[0,1280])
            y = np.interp(y2, [100,380],[0,1024])
            
            mouse.move(x,y,duration=0.1)

            cv2.rectangle(img, (100,100),(540,380) , (255,0,255) ,2)

        # left click
        elif fingers[1] == 1 and {fingers[i] for i in [0,2,3,4]} == {0}:
            mouse.click('left')
            
        # right click
        elif fingers[2] == 1 and {fingers[i] for i in [0,1,3,4]} == {0}:
            mouse.click('right')

        # right skip
        elif fingers[4] == 1 and {fingers[i] for i in [0,1,2,3]} == {0}:
            pyautogui.press('right')
        
        # left skip
        elif {fingers[i] for i in [1,2,3,4]} == {0} and fingers[0] == 1:
            pyautogui.press('left')
        
        # Scroll Downn
        elif {fingers[i] for i in [0,1,2]} == {1} and {fingers[i] for i in [3,4]} == {0}:
            mouse.wheel(-1)

        # Scroll Up
        elif {fingers[i] for i in [0,1,2,3]} == {1} and {fingers[i] for i in [4]} == {0}:
            mouse.wheel(1)

        # Volume Control
        elif {fingers[i] for i in [0,1,4]} == {1} and {fingers[i] for i in [2,3]} == {0}:
            x1,y1 = lmlist[4][1],lmlist[4][2] 
            x2,y2 = lmlist[8][1],lmlist[8][2]
            x,y = (x1+x2)//2 , (y1+y2)//2

    
            cv2.line(img, (x1,y1),  (x2,y2), (255,255,0), 2)
            cv2.circle(img,  (x,y), 5 , (255,255,0), cv2.FILLED)

            lineLength = math.hypot((x2-x1),(y2-y1))
            Vol =  np.interp(lineLength, [10,110], [-46.5,0])
            volBar =  np.interp(lineLength, [10,110], [400,150])
            volPer =  np.interp(lineLength, [10,110], [0,100])
            volume.SetMasterVolumeLevel(Vol , None)

            cv2.putText(img, f'{int(volPer)}%', (50,140), 5 , cv2.FONT_HERSHEY_PLAIN, (0), 2)


            if lineLength < 10:
                cv2.circle(img,  (x,y), 5 , (255,0,255), cv2.FILLED)
                volume.SetMasterVolumeLevel(-46.5 , None)

            if lineLength > 110:
                cv2.circle(img,  (x1,y1), 5 , (255,0,255), cv2.FILLED)
                cv2.circle(img,  (x2,y2), 5 , (255,0,255), cv2.FILLED)
        
            cv2.rectangle(img, (50 ,150),(75 ,400) , cv2.FILLED ,2)
            cv2.rectangle(img, (50 ,150),(75 ,400) , (0), 3)
            cv2.rectangle(img, (50 , int(volBar)),(75 ,400) , (0), cv2.FILLED)

            cv2.putText(img, f'{int(volPer)}%', (50,140), 5 , cv2.FONT_HERSHEY_PLAIN, (0), 2)

    cTime = time.time()
    fps = int(1/(cTime-pTime))
    pTime = cTime

    cv2.putText(img, f'FPS:{fps}', (10,25), 5 , cv2.FONT_HERSHEY_PLAIN, (0),2)

    cv2.imshow("Hand Controller",img)
    cv2.waitKey(1)    