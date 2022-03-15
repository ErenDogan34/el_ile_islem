import cv2
import mediapipe as mp
import pyttsx3 as pt

kamera = cv2.VideoCapture(0)

engine = pt.init()

mpHand = mp.solutions.hands

hands = mpHand.Hands()

mpDraw = mp.solutions.drawing_utils
checkThumbsUp = False

while True:
    success, image = kamera.read()

    imageRGB = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    hlms = hands.process(imageRGB)

    h,w,c = image.shape

    if hlms.multi_hand_landmarks:
        for handlandmarks in hlms.multi_hand_landmarks:

            for fingerNum, landmark in enumerate(handlandmarks.landmark):
                positionX,positionY = int(landmark.x*w),int(landmark.y*h)

                if fingerNum > 4 and landmark.y <handlandmarks.landmark[2].y:
                    break

                if fingerNum == 20 and landmark.y > handlandmarks.landmark[2].y:
                    checkThumbsUp = True

            mpDraw.draw_landmarks(image, handlandmarks, mpHand.HAND_CONNECTIONS)

    cv2.imshow("kamera",image)
    if checkThumbsUp:
            engine.say("screen turn off")
            engine.runAndWait()
            break
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break