import serial
import pymysql
import numpy as np
import time

r=[]

def connect_db(sql,action):
    
    cursor = db.cursor()
    if action == "u":
        cursor.execute(sql)
        db.commit()
    if action == "s":
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            r = row
        return r
    
def direction(f1):
    if f1 == 5 :
        comando = 's'
        #print('Quieto cachorro')
    if f1 == 1 :
        comando = 'l'
        #print('Izquierda')
    if f1 == 2 :
        comando = 'u'
        #print('Parriba')
    if f1 == 3 :
        comando = 'd'
        #print('Pabajo')
    if f1 == 4 :
        comando = 'r'
        #print('derecha')
    if f1 == 6 :
        comando = 'g'
        #print('Giro')
    if f1 == 7 :
        comando = 'o'
        #print('Opuesto')
        
    return comando


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
        

def align():
      
    heading_dif=np.abs(heading_x - heading);
    if heading_dif < 180:
        while heading_dif > 5: 
            d    = "o"
            arduino.write(d)
            data = arduino.readline()
            get_data(data)
            heading_dif=np.abs(heading_x - heading)
            if heading_dif < 5:
                d = "s"
                arduino.write(d)

    else:
        while heading_dif > 5 :
            d    = "g"
            arduino.write(d)
            data = arduino.readline()
            get_data(data)
            heading_dif=np.abs(heading_x - heading)
            if heading_dif < 5 :
                d = "s"
                arduino.write(d)

def calculus(frame):
    get_data(frame)
    own_latitude  = latitude*(10000/90)
    own_longitude = longitude*(40000/360)
    dlat          = (own_latitude-des_latitude)
    dlon          = (own_longitude-des_longitude)
    dist          = np.sqrt(dlat**2 + dlon**2)
    te            = (np.arctan2(dlon,dlat)) * 180/np.pi 
    heading_x     = normalization()
    heading_dif=np.abs(heading_x - heading)
    if heading_dif > 5:
        align()
    else:
        d = "u"
        arduino.write(d)
    route()

def normalization():
    #caso 1
    if (des_latitude > own_latitude) and (des_longitude < own_longitude):
        te = te+360
    #caso 2
    if (des_latitude == own_latitude) and (des_longitude < own_longitude):
        te = te+270;                                                                 
    #caso 3
    if (des_latitude < own_latitude) and (des_longitude < own_longitude):
        te = te+180;                                                                
    #caso 4
    if (des_latitude < own_latitude) and (des_longitude == own_longitude):
        te = te+180;                                                                 
    #caso 5
    if (des_latitude < own_latitude) and (des_longitude > own_longitude):
        te = te+180
    #caso 6
    if (des_latitude == own_latitude) and (des_longitude > own_longitude):
        te = te+90
    #caso 7
    if (des_latitude > own_latitude) and (des_longitude < own_longitude):
        te = te+0
    #caso 8
    if (des_latitude > own_latitude) and (des_longitude == own_longitude):
        te = te+0
    #caso 9
    else:
        te = te+0
        
    heading_x = te
    return heading_x;

def route():
  if dist <= 0.005:
        while(dist <= 0.005):
            d = "s"
            arduino.write(d)


arduino= serial.Serial('/dev/ttyUSB0',115200)
db = pymysql.connect("35.161.176.110","dante","12345","DORA-E")
print("Iniciando")
sql="UPDATE movements SET Mode=0"
connect_db(sql,"u")

latitude  = 0.0
longitude = 0.0
heading   = 0.0
te        = 0
x_lat     = 11.0207550
x_lon     = -74.8519370
des_latitude  = x_lat*(10000/90)
des_longitude = x_lon*(40000/360)
mode      = 0  
comando   = 's'
heading_x = 0

time.sleep(5)

while True:
    sql="SELECT Mode from movements"
    mode=connect_db(sql,"s")
    if mode[0] == 1 : 
        data=arduino.readline()
        print(data)
        get_data(data)
        arduino.flushInput()
        arduino.flush()
        arduino.flushOutput()

    else:
        
        sql="SELECT direction FROM movements"
        res=connect_db(sql,"s")
        d=direction(res[0])
        arduino.write(d)
        time.sleep(0.5)
        arduino.write('m')
        data=arduino.readline()
        print(data)
        get_data(data)
        arduino.flushInput()
        arduino.flush()
        arduino.flushOutput()
        

        
arduino.close()
db.close()
       
        
