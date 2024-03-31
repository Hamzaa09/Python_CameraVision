import cv2
import time
import math
import mediapipe as mp


class bodyTracking():
    def __init__(self, mode=False, model_complexity=1, smooth=True, 
                    enable_segmentation=False, smooth_segmentation=True, detection=0.5,
                    tracking=0.5):
        self.mode = mode
        self.model_complexity = model_complexity
        self.smooth = smooth
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.detection = detection
        self.tracking = tracking

        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.model_complexity, self.smooth,
                    self.enable_segmentation, self.smooth_segmentation, self.detection,
                    self.tracking)
        self.mpDraw = mp.solutions.drawing_utils

    def findPose(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.pose.process(imgRGB)

        if draw:
            if self.result.pose_landmarks:
                self.mpDraw.draw_landmarks(img, self.result.pose_landmarks,
                                        self.mpPose.POSE_CONNECTIONS)

        return img

    def getPositions(self, img):
        self.lmlist = []
        if self.result.pose_landmarks:
            for id,lm in enumerate(self.result.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy =  int(lm.x*w), int(lm.y*h)
                self.lmlist.append([id,cx,cy])

        return self.lmlist

    def getAngle(self, img, p1, p2, p3, draw=True):
        x1,y1 = self.lmlist[p1][1:] 
        x2,y2 = self.lmlist[p2][1:] 
        x3,y3 = self.lmlist[p3][1:] 

        angle = math.degrees(math.atan2(y3-y2 , x3-x2)-math.atan2(y1-y2 , x1-x2))
        if draw:
            cv2.line(img, (x1,y1), (x2,y2), (255,255,255), 2)
            cv2.line(img, (x2,y2), (x3,y3), (255,255,255), 2)

            cv2.circle(img, (x1,y1), 5, (255,0,255), cv2.FILLED)
            cv2.circle(img, (x1,y1), 10, (255,0,255),2)
            cv2.circle(img, (x2,y2), 5, (255,0,255), cv2.FILLED)
            cv2.circle(img, (x2,y2), 10, (255,0,255),2)
            cv2.circle(img, (x3,y3), 5, (255,0,255), cv2.FILLED)
            cv2.circle(img, (x3,y3), 10, (255,0,255),2)

        return angle

def main():
    cap = cv2.VideoCapture(0)
    detector = bodyTracking()

    pTime = 0
    while True:
        success, img = cap.read()
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        img = cv2.flip(img, 1)
        img = detector.findPose(img)
        lmlist = detector.getPositions(img)

        if lmlist:
            angle=detector.getAngle(img,12,14,16)
            # print(angle)

        cTime = time.time()
        fps = int(1/(cTime-pTime))
        pTime = cTime

        cv2.putText(img, str(fps), (10,20), 5, cv2.FONT_HERSHEY_PLAIN, (0,255,788))

        cv2.imshow("Video", img)
        cv2.waitKey(1)


if __name__=="__main__":
    main()