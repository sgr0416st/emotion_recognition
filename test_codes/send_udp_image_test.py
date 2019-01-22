import socket
import numpy as np
import cv2
from contextlib import closing

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
to_send_addr = ('127.0.0.1', 9999)

cap = cv2.VideoCapture(0)
size = (640, 360)

with closing(udp):
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret is False:
            break
        else:
            frame = cv2.resize(frame, size)
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            jpg_str = cv2.imencode('.jpeg', frame)
            # 画像を分割する
            # １つのデータが終了したよを伝えるために判断できる文字列を送信する
            # -> チェックするなら送信する画像のbytes数のほうがいいと思った
            for i in np.array_split(jpg_str[1], 20):
                # 画像の送信
                udp.sendto(i.tostring(), to_send_addr)
            udp.sendto(b'__end__', to_send_addr)

    udp.close()
    cap.release()
    cv2.destroyAllWindows()
