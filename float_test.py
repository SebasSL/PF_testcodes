

import serial
import pymysql
import numpy as np

r=[]

global s1          
global s2        
global s3        
global latitude  
global longitude 
global heading   
global speed     
global height    

s1        = 0  
s2        = 0
s3        = 0
latitude  = 0
longitude = 0
heading   = 0
speed     = 0
height    = 0

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
    
    global s1          
    global s2        
    global s3        
    global latitude  
    global longitude 
    global heading   
    global speed     
    global height
    
    s=frame.split(",")
    if len(s)>7:
        s[7] = s[7][:len(s[7])-1]
    if len(s)>7:
        for i in range(8):
            if len(s[i]) > 14 :
                s[i]=0
            else:
                s[i]=float(s[i])
        sql1 = "UPDATE sensorvalues SET"
        sql2 = " "
        
        
        if  5 < np.abs(s[0] - s1) :
            sql2 = sql2 + "sensor1= "+`s[0]`+" ,"

        if  5 < np.abs(s[1] - s2) :
            sql2 = sql2 + "sensor1= "+`s[1]`+" ,"

        if  5 < np.abs(s[2] - s3) :
            sql2 = sql2 + "sensor1= "+`s[2]`+" ,"

        if  5 < np.abs(s[3] - heading) :
            sql2 = sql2 + " heading= "+`s[3]`+" ,"

        if  0.000001 < np.abs(s[4] - latitude) :
            sql2 = sql2 + "latitude= "+`s[4]`+" ,"

        if  0.000001 < np.abs(s[5] - longitude) :
            sql2 = sql2 + "longitude= "+`s[5]`+" ,"

        if  2 < np.abs(s[6] - speed) :
            sql2 = sql2 + "Speed= "+`s[6]`+" ,"

        if  2 < np.abs(s[7] - height) :
            sql2 = sql2 + "Height= "+`s[7]`+" ,"

        s1        = s[0]    
        s2        = s[1]
        s3        = s[2]
        latitude  = s[4]
        longitude = s[5]
        heading   = s[3]
        speed     = s[6]
        height    = s[7]

        if len(sql2) > 10 :
            sql  = sql1 + sql2[:len(sql2)-1]
            connect_db(sql,"u")



arduino= serial.Serial('/dev/ttyUSB0',115200)
db = pymysql.connect("35.161.176.110","dante","12345","DORA-E")
cursor = db.cursor()



while True :
    data=arduino.readline()
    print(data)
    get_data(data)

arduino.close()
