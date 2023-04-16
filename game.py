import random
import os
import cv2
import numpy as np
import time 

folderPath = 'frames'
mylist = os.listdir(folderPath)
graphic = [cv2.imread(f'{folderPath}/{imPath}') for imPath in mylist]
green = graphic[0]
red = graphic[1]
kill = graphic[2]
winner = graphic[3]
intro = graphic[4]

cv2.imshow('squid game',cv2.resize(intro,(0,0),fx=0.69,fy=0.69))
cv2.waitKey(1)

while True:
    cv2.imshow('squid game',cv2.resize(intro,(0,0),fx=0.69,fy=0.69))
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

TIMER_MAX=30
TIMER=TIMER_MAX
maxMove=6500000
font=cv2.FONT_HERSHEY_SIMPLEX
cap=cv2.VideoCapture(0)
frameHeight=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
frameWidth=cap.get(cv2.CAP_PROP_FRAME_WIDTH)

win=False
prev=time.time()
showFrame=cv2.resize(green,(0,0),fx=0.69,fy=0.69)
isGreen = True

while cap.isOpened() and TIMER>=0:
    if isGreen and(cv2.waitKey(10) & 0xFF==ord('w')):
        win=True
        break
    ret,frame=cap.read()
    
    cv2.putText(showFrame,str(TIMER),(50,50),font,1,(0,int(255*(TIMER)/TIMER_MAX),int(255*(TIMER_MAX-TIMER)/TIMER)),4,cv2.LINE_AA)
    
    cur=time.time()
    no=random.randint(1,5)
    if cur-prev>=no:
        prev=cur
        TIMER=TIMER-no
        
        if cv2.waitKey(10) & 0xFF==ord('w'):
            win=True
            break
        
        if isGreen:
            showFrame=cv2.resize(red,(0,0),fx=0.69,fy=0.69)
            isGreen=False
            ref=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        else:
            showFrame=cv2.resize(green,(0,0),fx=0.69,fy=0.69)
            isGreen=True

    if not isGreen:

        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frameDelta = cv2.absdiff(ref,gray)
        thresh = cv2.threshold(frameDelta,20,255,cv2.THRESH_BINARY)[1]
        change = np.sum(thresh)
        if change>maxMove:
            break
    else:
        if cv2.waitKey(10) & 0xFF == ord('w'):
            win=True
            break

    camShow = cv2.resize(frame, (0,0), fx=0.4, fy= 0.4)

    camH, camW = camShow.shape[0],camShow.shape[1]
    showFrame[0:camH, -camW:] = camShow

    cv2.imshow('Squid Game', showFrame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

    if isGreen and (cv2.waitKey(10) & 0xFF==ord('w')):
        win = True
        break

cap.release()
if not win:

    while True:
        cv2.imshow('Squid Game',cv2.resize(kill,(0,0),fx=0.69,fy=0.69))

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
else:
    cv2.imshow('Squid Game', cv2.resize(winner,(0,0),fx=0.69,fy=0.69))
    cv2.waitKey(125)

    while True:
        cv2.imshow('Squid Game', cv2.resize(winner,(0,0),fx=0.69,fy=0.69))
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows