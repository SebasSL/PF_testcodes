import serial
import pymysql
import numpy as np
import time


r=[]

def connect_db(sql,action):
    
    if action == "u":
        cursor.execute(sql)
        db.commit()
    if action == "s":
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            r = row
        return r

def get_data(frame):
    s=frame.split(",")
    if len(s)>7:
        s[7] = s[7][:len(s[7])-1]
    if len(s)>7:
        for i in range(8):
            if len(s[i]) > 14 :
                s[i]=0
        
        latitude  = s[4]
        longitude = s[5]
        heading   = s[3]
        speed     = s[6]
        height    = s[7]
        
        sql1 = "UPDATE sensorvalues SET sensor1= "+`s[0]`+" , sensor2= "+`s[1]`+" , sensor3= "+`s[2]`+" , "
        sql2 = "latitude= "+`s[4]`+" , longitude= "+`s[5]`+" , heading= "+`s[3]`+" , Speed= "+`s[6]`+" , Height= "+`s[7]`
        sql  = sql1 + sql2
        connect_db(sql,"u")

arduino= serial.Serial('/dev/ttyUSB0',115200)
db = pymysql.connect("35.161.176.110","dante","12345","DORA-E")
cursor = db.cursor()

time.sleep(10)

while True :
    time.sleep(0.5)
    arduino.write('m')
    data=arduino.readline()
    print(data)
    get_data(data)
    arduino.flushInput()
    arduino.flush()
    arduino.flushOutput()

arduino.close()
