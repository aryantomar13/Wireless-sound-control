from ctypes.wintypes import PSMALL_RECT
import cv2
import mediapipe as mp
import math
import numpy
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap=cv2.VideoCapture(0)

while True:
    sucess, image=cap.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = []
            for id, lm in enumerate(handLms.landmark):
                #print(id, lm)
                h, w, c = image.shape
                cx, cy = int (lm.x*w), int(lm.y*h)
                #print(id, cx, cy)
                lmList.append([id,cx,cy])
                #print(lmlist)
        if lmList:
            x1 ,y1  = lmList[4][1] , lmList[4][2]
            x2, y2  = lmList[8][1], lmList[8][2]
            cv2.circle(image , (x1, y1) , 15 ,(134,23,42) , cv2.FILLED )
            cv2.circle(image , (x2, y2) , 15 ,(134,23,42) , cv2.FILLED )
            cv2.line(image , (x1 , y1) , (x2 , y2) ,(2 , 45 , 123) , 5)
            length = math.hypot(x2-x1 , y2-y1)
            print(length)
            z1 , z2 = (x1+x2)//2 , (y1+y2)//2
            
            if length<50 :
                cv2.circle(image , (z1 ,z2) ,25 , (4 , 123 , 142) ,cv2.FILLED)
            
            print(length)
            
            volume.GetMute()
        
        volRange  = volume.GetVolumeRange()
        minVol = volRange[0]
        maxVol = volRange[1]
        vol = numpy.interp(length , [50 ,300] , [minVol ,maxVol])
        print(vol)
        print(int(length) , vol)
        print(minVol ,maxVol)
        volume.SetMasterVolumeLevel(vol, None)
           # mp_drawing.draw_landmarks(image, handLms, mp_hands.HAND_CONNECTIONS)
    cv2.imshow("Hand",image)
    cv2.waitKey(1)