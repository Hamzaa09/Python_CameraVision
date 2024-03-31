import cv2 
import time 
import mediapipe as mp 

cap = cv2.VideoCapture(0)

mpface = mp.solutions.face_detection
faceDetection = mpface.FaceDetection(.75) 
# mpDraw = mp.solutions.drawing_utils

pTime = 0
while True:
    success, img = cap.read()
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
    result = faceDetection.process(imgRGB)
    # print(result)

    if result.detections:
        for id,detection in enumerate(result.detections):
            # mpDraw.draw_detection(img,detection)
            # print(id,detection)
            h, w, c = img.shape
            bboxC = detection.location_data.relative_bounding_box
            bbox = int(bboxC.xmin*w),int(bboxC.ymin*h), \
                    int(bboxC.width*w),int(bboxC.height*h)
            cv2.rectangle(img, bbox, (255,0,255), 2,3)
            cv2.putText(img, f'{int(detection.score[0]*100)}%', (bbox[0],bbox[1]-20), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,788), 2)


    cTime = time.time()
    fps = int(1/(cTime-pTime))
    pTime = cTime

    cv2.putText(img, str(fps), (10,20), 5, cv2.FONT_HERSHEY_PLAIN, (0,255,788))

    cv2.imshow("Face Detection", img)
    cv2.waitKey(1)