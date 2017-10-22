import threading
import serial
import time

arduino= serial.Serial('/dev/ttyUSB0',115200)
r=[]
leer = 0
data="0,0,0,0,0,0,0,0"


def db_main():
    while True:
        leer=1
        time.sleep(0.2)
        print(data)
        time.sleep(0.3)

def obtain_data():
    global leer 
    while True:
        if leer == 1:
            arduino.write('m')
            data=arduino.readline()
            print(data)
            leer=leer-1

time.sleep(10)


th1=threading.Thread(target=db_main,name="meh1")
th2=threading.Thread(target=obtain_data,name="meh2")



th1.start()
th2.start()


