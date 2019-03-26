import os
import time

pre = time.time()+2
while True:
    
    curr = time.time()

    if curr-pre > 0.01:
        os.system('sudo scp -i /home/pi/.ssh/MyKeyPair.pem  /dev/shm/mjpeg/cam.jpg  ubuntu@35.161.176.110:/var/www/html/DORA-E/')
        pre=curr
