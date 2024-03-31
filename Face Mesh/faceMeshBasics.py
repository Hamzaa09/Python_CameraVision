import cv2
import time 
import mediapipe as mp 


cap = cv2.VideoCapture(0)

mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(2)
mpDraw = mp.solutions.drawing_utils
drawSpecs = mpDraw.DrawingSpec((0,255,0), thickness=1, circle_radius=1)

while True:
    success, img = cap.read()
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img = cv2.flip(img, 1)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    result = faceMesh.process(imgRGB)

    if result.multi_face_landmarks:
        for facelms in result.multi_face_landmarks:
            for id,lms in enumerate(facelms.landmark):
                h , w, c= img.shape
                cx ,cy = int(lms.x*w),int(lms.y*h)
                # print(id,cx,cy)
            mpDraw.draw_landmarks(img, facelms, mpFaceMesh.FACEMESH_RIGHT_EYE, drawSpecs)

    cv2.imshow("FaceDetection Basics", img)
    cv2.waitKey(1)