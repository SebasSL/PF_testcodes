import cv2
import numpy as np
import time
import serial
import os

sq2=np.ones((9,9))


def color_chase(frame):
    
    img=frame.copy()
    img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    low=np.array([100,50,30])
    up=np.array([140,255,255])
    mask=cv2.inRange(img_hsv,low,up)
    out=cv2.bitwise_and(frame,frame,mask=mask)
    out=cv2.erode(out,sq2,iterations=1)
    out=cv2.dilate(out,sq2,iterations=1)
    return out
    
def draw(frame, out):
    try:
        im=out.copy()
        imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(imgray,10,255,0)
        _, contours, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        x1=640
        y1=360
        x2=0
        y2=0
        a=[]
        b=[a.append(cnt) for cnt in contours]
        for i in range(len(a[0])):
            if a[0][i][0][0]<x1:
                x1=a[0][i][0][0]
            if a[0][i][0][1]<y1:
                y1=a[0][i][0][1]
            if a[0][i][0][0]>x2:
                x2=a[0][i][0][0]
            if a[0][i][0][1]>y2:
                y2=a[0][i][0][1]
        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2);
    except:
        pass

#vs = PiVideoStream().start()

arduino= serial.Serial('/dev/ttyUSB0',115200)
i=0
dirname=str(time.time())
os.makedirs(dirname)
time.sleep(2.0)
while i < 10:
    i=i+1
    d=b"g"
    arduino.write(d)
    time.sleep(0.2)
    d=b"s"
    arduino.write(d)
    time.sleep(1)
    frame = cv2.imread("/dev/shm/mjpeg/cam.jpg",cv2.IMREAD_COLOR)
    orig = frame.copy()
    blue = color_chase(frame)
    draw(frame,blue)
    print(i)
    name = "image "+str(i)
    cv2.imwrite(name+".jpg",frame)
    cv2.imwrite(name+" blue.jpg",orig)
    os.rename("/home/pi/Codes/frames/"+name+".jpg", "/home/pi/Codes/frames/"+dirname+"/"+name+".jpg")
    os.rename("/home/pi/Codes/frames/"+name+" blue.jpg", "/home/pi/Codes/frames/"+dirname+"/"+name+" blue.jpg")
    time.sleep(1)
    
    print(i)


