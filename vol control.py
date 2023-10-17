   #importing all the required libraries
import cv2
import mediapipe as mp
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

cap = cv2.VideoCapture(0) #Checks for camera
mpHands = mp.solutions.hands #detects hand/finger
hands = mpHands.Hands()   #complete the initialization configuration of hands
mpDraw = mp.solutions.drawing_utils

#mpstyle = mp.solutions.drawing_styles
#To access speaker through the library pycaw 
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volbar=400
volper=0
volMin,volMax = volume.GetVolumeRange()[:2]
while True:
    success,img = cap.read() #If camera works capture an image
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #Convert to rgb  
    #Collection of gesture information
    results = hands.process(imgRGB) #completes the image processing.
    lmList = [] #empty list
    if results.multi_hand_landmarks: #list of all hands detected.
        for handlandmark in results.multi_hand_landmarks:
            for id,lm in enumerate(handlandmark.landmark): #adding counter and returning it
                # Get finger joint points
                h,w,_ = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                lmList.append([id,cx,cy]) #adding to the empty list 'lmList'
            mpDraw.draw_landmarks(img,handlandmark,mpHands.HAND_CONNECTIONS)
    if lmList != []:
        #getting the value at a point
                        #x      #y
        x1,y1 = lmList[4][1],lmList[4][2]  #thumb
        x2,y2 = lmList[8][1],lmList[8][2]  #index finger
        #creating circle at the tips of thumb and index finger
        cv2.circle(img,(x1,y1),13,(48,25,52),cv2.FILLED) #image #fingers #radius #rgb
        cv2.circle(img,(x2,y2),13,(48,25,52),cv2.FILLED) #image #fingers #radius #rgb
        cv2.line(img,(x1,y1),(x2,y2),(48,25,60),3)  #create a line b/w tips of index finger and thumb
        length = hypot(x2-x1,y2-y1) #distance b/w tips using hypotenuse
 # from numpy we find our length,by converting hand range in terms of volume range ie b/w 20 to 225
        vol = np.interp(length,[20,225],[volMin,volMax]) 
        volbar=np.interp(length,[20,225],[400,150])
        volper=np.interp(length,[20,255],[0,100])
        print(vol,int(length))
        volume.SetMasterVolumeLevel(vol, None)
        vol=vol
        # Hand range 20 - 225
        # Volume range -96 - 0.0
        #creating volume bar for volume level 
        cv2.rectangle(img,(50,150),(85,400),(0,255,255),4) # vid ,initial position ,ending position ,rgb ,thickness
        cv2.rectangle(img,(50,int(volbar)),(85,400),(255,90,70),cv2.FILLED)
        cv2.putText(img,f"{int(volper)}%",(10,40),cv2.FONT_ITALIC,1,(48, 213, 200),3)
        #tell the volume percentage ,location,font of text,length,rgb color,thickness
    cv2.imshow('Image',img) #Show the video 
    if cv2.waitKey(1) & 0xff==ord(' '): #By using spacebar delay will stop
        break
        
cap.release()     #stop cam       
cv2.destroyAllWindows() #close window
'''CLICK SPACE BAR IN ORDER TO STOP THE PROGRAM'''