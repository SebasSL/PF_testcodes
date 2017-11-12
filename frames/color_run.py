import cv2
import numpy as np
import time
import serial
import os

sq2=np.ones((9,9))


def color_chase(frame):
    
    img=frame.copy()
    img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    low=np.array([110,50,30])
    up=np.array([130,255,255])
    mask=cv2.inRange(img_hsv,low,up)
    out=cv2.bitwise_and(frame,frame,mask=mask)
    out=cv2.erode(out,sq2,iterations=1)
    out=cv2.dilate(out,sq2,iterations=1)
    return out
    
def draw(frame, out):
    try:
        im=out.copy()
        imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(imgray,20,255,0)
        _, contours, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        a=[]
        b=[a.append(cnt) for cnt in contours]
        x1=640*np.ones((1,len(a)))
        y1=360*np.ones((1,len(a)))
        x2=np.zeros((1,len(a)))
        y2=np.zeros((1,len(a)))
        area = 0
        for i in range(len(a)):
            for j in range(len(a[i])):
                if a[i][j][0][0]<x1[i]:
                    x1[i]=a[i][j][0][0]
                if a[i][j][0][1]<y1[i]:
                    y1[i]=a[i][j][0][1]
                if a[i][j][0][0]>x2[i]:
                    x2[i]=a[i][j][0][0]
                if a[i][j][0][1]>y2[i]:
                    y2[i]=a[i][j][0][1]
            
            if area < (x2[i]-x1[i])*(y2[i]-y1[i]):
                xi = x1[i]
                yi = y1[i]
                xf = x2[i]
                yf = y2[i]
                area = (x2[i]-x1[i])*(y2[i]-y1[i])
        
        cv2.rectangle(frame,(xi,yi),(xf,yf),(0,255,0),2);
        return area
    except:
        pass

#vs = PiVideoStream().start()

arduino= serial.Serial('/dev/ttyACM0',115200)
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
    area = draw(frame,blue)
    print(i)
    print(area)
    name = "image "+str(i)
    cv2.imwrite(name+".jpg",frame)
    cv2.imwrite(name+" blue.jpg",orig)
    os.rename("/home/pi/Codes/frames/"+name+".jpg", "/home/pi/Codes/frames/"+dirname+"/"+name+".jpg")
    os.rename("/home/pi/Codes/frames/"+name+" blue.jpg", "/home/pi/Codes/frames/"+dirname+"/"+name+" blue.jpg")
    try:
        if area > 0:
            os.rename("/home/pi/Codes/frames/"+dirname+"/"+name+".jpg", "/home/pi/Codes/frames/"+dirname+"/cam.jpg")
            os.system('sudo scp -i /home/pi/.ssh/MyKeyPair.pem  /dev/shm/mjpeg/cam.jpg  ubuntu@35.161.176.110:/var/www/html/DORA-E/')
            i = 10
    except:
        pass
    time.sleep(1)
    
    print(i)


