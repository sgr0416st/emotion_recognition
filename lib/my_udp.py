import socket
import numpy as np
import cv2
import math


PORT_VIDEO = 10001
PORT_AUDIO = 10002

# あんま大きいのはよくないらしい
MAX_PACKET_SIZE = 9000
MAGIC_WORD = b'__end__'


class Sender:
    def __init__(self, send_IP, send_port):
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.to_send_addr = (send_IP, send_port)

    def send(self, data):
        self.udp.sendto(data, self.to_send_addr)

    def send_image(self, frame):
        jpg_str = cv2.imencode('.jpeg', frame)
        size = jpg_str[1].nbytes
        packet_num = max(math.ceil(size / MAX_PACKET_SIZE), 1)
        # 画像を分割する
        # １つのデータが終了したよを伝えるために判断できる文字列を送信する
        # -> チェックするなら送信する画像のbytes数のほうがいいと思った
        for i in np.array_split(jpg_str[1], packet_num):
            # 画像の送信
            self.send(i.tostring())
        self.send(MAGIC_WORD)

    def close(self):
        self.udp.close()


class Receiver:
    def __init__(self, receive_IP, receive_port):
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.bind((receive_IP, receive_port))

    def receive_image(self):
        buff = MAX_PACKET_SIZE + 1
        while True:
            recive_data = bytes()
            while True:
                # 送られてくるデータが大きいので一度に受け取るデータ量を大きく設定
                jpg_str, addr = self.udp.recvfrom(buff)
                is_len = len(jpg_str) == len(MAGIC_WORD)
                is_end = jpg_str == MAGIC_WORD
                if is_len and is_end: break
                recive_data += jpg_str

            if len(recive_data) == 0: continue

            # string型からnumpyを用いuint8に戻す
            narray = np.fromstring(recive_data, dtype='uint8')
            # uint8のデータを画像データに戻す
            img = cv2.imdecode(narray, 1)
            yield img

    def receive(self):
        buff = MAX_PACKET_SIZE + 1
        while True:
            receive_data, addr = self.udp.recvfrom(buff)
            if len(receive_data) == 0: continue
            yield receive_data

    def close(self):
        self.udp.close()
