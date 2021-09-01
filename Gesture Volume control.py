# Filter based on size
# Will find the distance between the index and thumb
# Convert volume
# Reduce resolution to make it smoother
# Check which of the fingers are up
# if pinky is down set vol
# Drawings
# frame rate
'''This is our raw code but its working we will add more creality and the above measures in future to this 
project.'''          

import cv2
import mediapipe as mp
import time
import HandTrackingmodule as htm
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
 
################################
wCam, hCam = 640, 480
################################
pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
Detector = htm.handDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

while True:
    success, img = cap.read()

    # find hand
    img = Detector.findHands(img, )
    lmList = Detector.findPosition(img, draw=False)
    if len(lmList) != 0:  
        #print(lmList[4], lmList[8]) 

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        Length = math.hypot(x2 - x1, y2 - y1)
        #print(Length)

        # Hand range 18 - 290
        # Volume range -65 - 0

        vol = np.interp(Length,[28,180], [minVol, maxVol])
        volBar = np.interp(Length,[28,180], [400, 150])
        volPer = np.interp(Length,[28,180], [0, 100])
        print(int(Length), vol)
        volume.SetMasterVolumeLevel(vol, None)

        if Length<50:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(img, (50, 150), (85, 400), (255, 234, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f': {int(volPer)}', (40,450), cv2.FONT_HERSHEY_COMPLEX,1, (255, 234, 0 ),3)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (10,70), cv2.FONT_HERSHEY_COMPLEX,1, (255, 234, 0 ),3)
    cv2.imshow("Image", img )
    cv2.waitKey(1)

