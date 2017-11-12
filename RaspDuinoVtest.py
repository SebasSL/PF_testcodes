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
        print('Quieto cachorro')
    if f1 == 1 :
        comando = 'l'
        print('Izquierda')
    if f1 == 2 :
        comando = 'u'
        print('Parriba')
    if f1 == 3 :
        comando = 'd'
        print('Pabajo')
    if f1 == 4 :
        comando = 'r'
        print('derecha')
    if f1 == 6 :
        comando = 'g'
        print('Giro')
    if f1 == 7 :
        comando = 'o'
        print('Opuesto')
        
    return comando


def get_data(frame):
    s=frame.split(",")
    if len(s)>7:
        s[7] = s[7][:len(s[7])-1]
    if len(s)>7:
        for i in range(8):
            if len(s[i]) > 14 :
                s[i]=0
	try:        
	    heading   = float(s[3])
            latitude  = float(s[4])
            longitude = float(s[5])
            speed     = float(s[6])
            height    = float(s[7])
	except:
	    heading   = 0
	    latitude  = 0
            longitude = 0
	    speed     = 0
	    height    = 0

        sql1 = "UPDATE sensorvalues SET sensor1= "+`s[0]`+" , sensor2= "+`s[1]`+" , sensor3= "+`s[2]`+" , "
        sql2 = "latitude= "+`s[4]`+" , longitude= "+`s[5]`+" , heading= "+`s[3]`+" , Speed= "+`s[6]`+" , Height= "+`s[7]`
        sql  = sql1 + sql2
        connect_db(sql,"u")
        return [latitude,longitude,heading,s[0],s[1],s[2]]

def align(heading_x,heading):
    
    heading_dif = heading_x - heading
    print(heading_dif)
    if heading_dif < 180 and  heading_dif > 0 :
        while np.abs(heading_dif) >8: 
            d    = "r"
            print(d)
            arduino.write(d)
            time.sleep(0.5)
            arduino.write('m')
            data = arduino.readline()
            print(data)
            [latitude,longitude,heading,s1,s2,s3] = get_data(data)
            arduino.flushInput()
            arduino.flush()
            arduino.flushOutput()
            heading_dif=np.abs(heading_x - heading)
            print(heading_dif, heading_x, heading)
            if heading_dif < 8:
                d = "s"
                print(d)
                arduino.write(d)
		time.sleep(0.5)

    else:
        while np.abs(heading_dif) > 8:
            d    = "l"
            print(d)
            arduino.write(d)
            time.sleep(0.5) 
            arduino.write('m')
            data = arduino.readline()
            print(data)
            [latitude,longitude,heading,s1,s2,s3] = get_data(data)
            arduino.flushInput()
            arduino.flush()
            arduino.flushOutput()
            heading_dif=np.abs(heading_x - heading)
            print(heading_dif, heading_x, heading)
            if heading_dif < 8:
                d = "s"
                print(d)
                arduino.write(d)
		time.sleep(0.5)

def calculus(frame):
    [latitude,longitude,heading,s1,s2,s3] = get_data(frame)
    
    own_latitude  = latitude*(10000/90)
    own_longitude = longitude*(40000/360)
    dlat          = (own_latitude-des_latitude)
    dlon          = (own_longitude-des_longitude)
    dist          = np.sqrt(dlat**2 + dlon**2)
    te            = (np.arctan(dlon/dlat)) * 180/np.pi 
    heading_x     = normalization(own_latitude,own_longitude,te)
    heading_dif=np.abs(heading_x - heading)
    print(heading_dif,dist*1000)
    if heading_dif > 15:
        align(heading_x,heading)
    else:
        d = "u"
        print(d)
        arduino.write(d)
    
    route(dist)

def normalization(own_latitude,own_longitude,te):
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

def obs_action(heading):
    h1=heading
    h=0
    d = "d" 
    arduino.write(d)
    time.sleep(1)
    while (np.abs(h1-h)<90):
        arduino.write("m")
        data = arduino.readline()
        print(data)
        [_,_,h,_,_,_]=get_data(data)
        arduino.flushInput()
        arduino.flush()
        arduino.flushOutput()
        print(np.abs(h1-h))
        d="l"
        arduino.write(d)

    time.sleep(0.5)
    d = "r"
    arduino.write(d)
    time.sleep(0.5)    


def route(dist):
    if dist <= 0.005:
        print("Llegueeee :D")
        while(dist <= 0.005):
            d = "s"
            arduino.write(d)
            


arduino= serial.Serial('/dev/ttyACM0',115200)
db = pymysql.connect("35.161.176.110","dante","12345","DORA-E")
print("Iniciando")
sql="UPDATE movements SET Mode=0"
connect_db(sql,"u")
sqls = "SELECT latitude , longitude FROM destination"
[x_lat, x_lon] = connect_db(sqls, "s")

s1        = 0
s2        = 0
s3        = 0
obs       = 0 
meh       = 1
latitude  = 0.0
longitude = 0.0
heading   = 0.0
te        = 0
des_latitude  = float(x_lat)*(10000/90)
des_longitude = float(x_lon)*(40000/360)
mode      = 0  
comando   = 's'
heading_x = 0

time.sleep(5)





while True:
    sql="SELECT Mode from movements"
    mode=connect_db(sql,"s")
    if mode[0] == 1 :
        if meh == 1 : 
            time.sleep(0.3)
            arduino.write('m')
            data=arduino.readline()
            print(data)
            [latitude,longitude,heading,s1,s2,s3] = get_data(data)
            arduino.flushInput()
            arduino.flush()
            arduino.flushOutput()
            d = "u"
            arduino.write(d)
            num = 0
            while num < 7 :
                time.sleep(0.3)
                arduino.write('m')
                data=arduino.readline()
                print(data,num)
                [latitude,longitude,heading,s1,s2,s3] = get_data(data)
                arduino.flushInput()
                arduino.flush()
                arduino.flushOutput()
                num = num + 1
            d = "d"
            arduino.write(d)
            num = 0
            while num < 4 :
                time.sleep(0.3)
                arduino.write('m')
                data=arduino.readline()
                print(data,num)
                [latitude,longitude,heading,s1,s2,s3] = get_data(data)
                arduino.flushInput()
                arduino.flush()
                arduino.flushOutput()
                num = num + 1
            d = "l"
            arduino.write(d)
            num = 0
            while num < 8 :
                time.sleep(0.3)
                arduino.write('m')
                data=arduino.readline()
                print(data,num)
                [latitude,longitude,heading,s1,s2,s3] = get_data(data)
                arduino.flushInput()
                arduino.flush()
                arduino.flushOutput()
                num = num + 1
            d = "r"
            arduino.write(d)
            num = 0
            while num < 8 :
                time.sleep(0.3)
                arduino.write('m')
                data=arduino.readline()
                print(data,num)
                [latitude,longitude,heading,s1,s2,s3] = get_data(data)
                arduino.flushInput()
                arduino.flush()
                arduino.flushOutput()
                num = num + 1
            meh = 0
            
            

        time.sleep(0.3)
        arduino.write('m')
        data=arduino.readline()
        print(data)
        calculus(data)
        
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
       
        
