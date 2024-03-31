import cv2 
import time 
import mediapipe as mp 

class FaceDetector():
    def __init__(self, detectionCon=0.5, model_selection=1):
        self.detectionCon = detectionCon
        self.model_selection = model_selection
        self.mpface = mp.solutions.face_detection
        self.faceDetection = self.mpface.FaceDetection(self.detectionCon, self.model_selection) 


    def faceDetection(self, img, draw=True):
            imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
            self.result = self.faceDetection.process(imgRGB)

            if self.result.detections:
                bboxs = []
                for id,detection in enumerate(self.result.detections):
                    h, w, c = img.shape
                    bboxC = detection.location_data.relative_bounding_box
                    bbox = int(bboxC.xmin*w), int(bboxC.ymin*h), int(bboxC.width*w),int(bboxC.height*h)
                    bboxs.append([id,bbox,detection.score])
                    if draw:
                        cv2.rectangle(img, bbox, (255,0,255), 2,3)
                        cv2.putText(img, f'{int(detection.score[0]*100)}%', (bbox[0],bbox[1]-20), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,788), 2)
            return img,bboxs

def main():
    cap = cv2.VideoCapture(0)
    detector = FaceDetector()
    
    pTime = 0
    while True:
        success, img = cap.read()
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        img = cv2.flip(img, 1)
        img,bboxs = detector.faceDetection(img)


        cTime = time.time()
        fps = int(1/(cTime-pTime))
        pTime = cTime

        cv2.putText(img, str(fps), (10,20), 5, cv2.FONT_HERSHEY_PLAIN, (0,255,788))

        cv2.imshow("Face Detection", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()