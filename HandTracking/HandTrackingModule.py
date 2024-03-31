import cv2
import time
import mediapipe as mp


class handDetector():
    def __init__(self, mode=False, maxHands=2, model_complexity=1, 
                            detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxhands = maxHands
        self.model_complexity = model_complexity
        self.detectionCon = detectionCon
        self.trackingCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxhands, self.model_complexity,
                                        self.detectionCon, self.trackingCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipList = [8,12,16,20]


    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.result = self.hands.process(imgRGB)

        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
        
    def findPosition(self, img, handno=0, draw=False):
        self.lmlist = []
        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handno] 
            for id,hlms in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(hlms.x * w), int(hlms.y * h)
                self.lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)
            return self.lmlist

    def fingersCounter(self,draw=False):
        if self.lmlist:
            fingerUpList = []
            if self.lmlist[4][1] < self.lmlist[2][1]:
                fingerUpList.append(1)
            else:
                fingerUpList.append(0)

            for id in range(4):
                if self.lmlist[self.tipList[id]][2] < self.lmlist[self.tipList[id]-2][2]:
                    fingerUpList.append(1)
                else:
                    fingerUpList.append(0)
            if draw:
                cv2.rectangle(img, (0,400),(80,600), (0), cv2.FILLED)
                cv2.putText(img, f'{fingerUpList.count(1)}', (30,450), cv2.FONT_HERSHEY_PLAIN , 2, (255), 2)
            return fingerUpList
 
def main():
    video = cv2.VideoCapture(0)
    detector = handDetector()

    cTime = 0
    pTime = 0

    while True:
        success, img = video.read()
        img = detector.findHands(img)
        # img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        img = cv2.flip(img,1)

        lmlist = detector.findPosition(img)
        fingers = detector.fingersCounter()
        if lmlist:
            # print(lmlist)
            print(fingers)

        cTime = time.time()
        fps = int(1/(cTime-pTime))
        pTime = cTime

        cv2.putText(img, str(fps), (10,25), 5 , cv2.FONT_HERSHEY_PLAIN, (0,255,255))

        cv2.imshow("Image ", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()