from lib.my_udp import Sender
import cv2

IP = '127.0.0.1'
port = 9999
sender = Sender(IP, port)

cap = cv2.VideoCapture(0)
size = (640, 360)
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret is False:
        break
    else:
        frame = cv2.resize(frame, size)
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        sender.send_image(frame)

sender.close()
cap.release()
cv2.destroyAllWindows()

