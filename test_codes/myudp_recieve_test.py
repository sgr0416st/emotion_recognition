from lib.my_udp import Receiver
import cv2

IP = '127.0.0.1'
port = 9999
receiver = Receiver(IP, port)

# 画像を取り続ける
for img in receiver.receive_image():
    # 送信された画像の処理を行う
    # ...
    cv2.imshow("frame", img)
    # Enterキーで終了
    if cv2.waitKey(10) == 13:
        break

receiver.close()
cv2.destroyAllWindows()

