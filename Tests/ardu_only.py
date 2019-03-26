import serial
import time
import to_db


arduino= serial.Serial('/dev/ttyUSB0',115200)
time.sleep(10)

while True :
    arduino.write('s')
    print('s')
    data=arduino.readline()
    print(data)
    
arduino.write('s')
arduino.close()
