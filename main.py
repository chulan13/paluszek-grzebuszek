import HandTrackingModule
import mediapipe as mp
import cv2
import numpy as np
import math
import time
from pyfirmata import Arduino, SERVO, util

pin = 10
port = 'ur port (take a look at arduino ide)'
arduino = Arduino(port)

arduino.digital[pin].mode = SERVO

def rotateservo(pin, angle):
    arduino.digital[pin].write(angle)
    time.sleep(0.0015)

pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)

detector = HandTrackingModule.handDetector(maxHands=1)

while True:
    success, img = cap.read()
    hand = detector.findHands(img)
    lmList = detector.findPos(img)
    arr = []
    if len(lmList) != 0:

        
        p9_p12 = detector.findDistance(img, 9, 12)
        p0_p12 = detector.findDistance(img, 0, 12)
        for i in range(0, len(p9_p12)):
            for j in range(0, len(p0_p12)):
                arr.append(p9_p12[i]/p0_p12[i])
        dist = arr[0]

        
        angle_less_than_1 = int(dist*360)

        

        if dist > 0.44 and dist < 0.5:
           rotateservo(pin, 0)
        else: 
            if dist>=0 and dist<=1:
                
                rotateservo(pin, angle_less_than_1)
            else:
                print(angle_less_than_1)


            
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

        
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
