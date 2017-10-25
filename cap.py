import cv2
from picamera.array  import PiRGBArray
from picamera import PiCamera
import time

camera = PiCamera()
rawCapture = PiRGBArray(camera)

time.sleep(0.1)

camera.capture(rawCapture , format="bgr")
image = rawCapture.array

image=cv2.resize(image,(640,360),interpolation = cv2.INTER_CUBIC)

cv2.imshow("image",image)
cv2.waitKey(0)




