import serial
import pymysql

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
    if f1 == 1 :
        comando = 'l'
    if f1 == 2 :
        comando = 'u'
    if f1 == 3 :
        comando = 'd'
    if f1 == 4 :
        comando = 'r'
    if f1 == 6 :
        comando = 'g'
    if f1 == 7 :
        comando = 'o'
        
    if comando == 'u':
        print('Parriba')
    elif comando == 'd':
        print('Pabajo')
    if comando == 'r':
        print('derecha')
    elif comando == 'l':
        print('Izquierda')
    if comando == 'g':
        print('Giro')
    elif comando == 'o':
        print('Opuesto')
    if comando == 's':
        print('Quieto cachorro')
    return comando


def get_data(frame):
    s=frame.split(",")
    if len(s)>3:
        s[3] = s[3][:len(s[3])-1]
    print(s)
    if len(s)>3:
        
        sql="UPDATE sensorvalues SET sensor1= "+`s[0]`+" , sensor2= "+`s[1]`+" , sensor3= "+`s[2]`+" , sensor4= "+`s[3]`
        connect_db(sql,"u")
        
arduino= serial.Serial('/dev/ttyUSB0',115200)
db = pymysql.connect("35.161.176.110","dante","12345","DORA-E")
print("Iniciando1")
comando = 's'
while True:

    sql="SELECT direction FROM movements"
    res=connect_db(sql,"s")
    print("test1")
    d=direction(res[0])
    arduino.write(d)
    print("test3")
    data=arduino.readline()
    print("test2")
    get_data(data)
    
        
arduino.close()
db.close()
       
        
