import cv2
import time 
import mediapipe as mp 


class FaceMeshDetector():
    def __init__(self, imgMode=False, maxfaces=2, refine_landmarks=False, detectionCon=0.5,         trackingCon=0.5):

        self.imgMode = imgMode
        self.maxfaces = maxfaces
        self.refine_landmarks = refine_landmarks
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon

        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.imgMode, self.maxfaces, self.refine_landmarks,self.detectionCon, self.trackingCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.drawSpecs = self.mpDraw.DrawingSpec((0,255,0), thickness=1, circle_radius=1)

    def face_Mesh(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.faceMesh.process(imgRGB)
        faces = []

        if self.result.multi_face_landmarks:
            for facelms in self.result.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, facelms, self.mpFaceMesh.FACEMESH_RIGHT_EYE, self.drawSpecs)
                    face = []
                    for id,lms in enumerate(facelms.landmark):
                        h , w, c= img.shape
                        cx ,cy = int(lms.x*w),int(lms.y*h)
                        face.append([cx,cy])
                faces.append(face)
        return img, faces

def main():
    cap = cv2.VideoCapture(0)
    detector = FaceMeshDetector()

    while True:
        success, img = cap.read()
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        img = cv2.flip(img, 1)
        img,faces = detector.face_Mesh(img)
        if faces:
            print(len(faces))

        cv2.imshow("FaceDetection Basics", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()