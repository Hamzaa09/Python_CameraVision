import cv2
import time
import mediapipe as mp

cap = cv2.VideoCapture(0)
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

pTime = 0
while True:
    success, img = cap.read()
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = pose.process(imgRGB)

    if result.pose_landmarks:
        mpDraw.draw_landmarks(img, result.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id,lm in enumerate(result.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy =  int(lm.x*w), int(lm.y*h)
            # if id == 4:
            #     print(id, cx, cy)


    cTime = time.time()
    fps = int(1/(cTime-pTime))
    pTime = cTime

    cv2.putText(img, str(fps), (10,30), 2, cv2.FONT_HERSHEY_PLAIN, (0,255,788))

    cv2.imshow("Video", img)
    cv2.waitKey(1)