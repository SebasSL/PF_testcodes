
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import cv2


vs = PiVideoStream().start()
time.sleep(2.0)

while True:
    
    frame = vs.read()
    frame = imutils.resize(frame, width=720)
 
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break
    
 
cv2.destroyAllWindows()
vs.stop()
