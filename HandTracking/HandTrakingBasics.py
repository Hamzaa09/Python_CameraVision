import cv2
import time
import mediapipe as mp

video = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

cTime = 0
pTime = 0

while True:
    success, img = video.read()
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img = cv2.flip(img,1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(imgRGB)


    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            print(handLms.landmark)
            # for id,hlms in enumerate(handLms.landmark):
            #     h, w, c = img.shape
            #     cx, cy = int(hlms.x * w), int(hlms.y * h)
            #     if (id == 16): 
            #         cv2.circle(img, (cx, cy), 10, (0,255,0), cv2.FILLED)                
            # mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)


    cTime = time.time()
    fps = int(1/(cTime-pTime))
    pTime = cTime

    cv2.putText(img, str(fps), (10,25), 5 , cv2.FONT_HERSHEY_PLAIN, (0,255,255))

    cv2.imshow("Image ", img)
    cv2.waitKey(1)