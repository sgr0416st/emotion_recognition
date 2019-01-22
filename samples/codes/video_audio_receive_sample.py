from samples.codes.audio_receive_sample import audio_receive
import threading
import lib.my_udp as udp
import lib.network_data as ip
import cv2


class ConditionalFlag:
    def __init__(self):
        self._flag = False
        self._condition = threading.Condition()

    def set_true(self):
        with self._condition:
            self._flag = True
            self._condition.notify_all()

    def set_false(self):
        with self._condition:
            self._flag = False

    def wait_until_true(self):
        with self._condition:
            while not self._flag:  # 条件がFalseか判定
                self._condition.wait()  # ブロック
            self._flag = False


if __name__ == "__main__":
    receive_IP = ip.mac_IP
    send_IP = ip.mac_pro_IP

    image = None
    img_rc_flag = ConditionalFlag()

    def _video_receive(_IP):

        global image
        global img_rc_flag

        port = udp.PORT_VIDEO
        receiver = udp.Receiver(_IP, port)
        for img in receiver.receive_image():
            if img is None:
                continue
            else:
                image = img
                img_rc_flag.set_true()

        receiver.close()
        cv2.destroyAllWindows()

    thread_video = threading.Thread(target=_video_receive, args=([receive_IP]))
    thread_audio = threading.Thread(target=audio_receive, args=([receive_IP]))
    thread_video.start()
    thread_audio.start()

    # 送信された画像の処理を行う
    while True:
        img_rc_flag.wait_until_true()
        cv2.imshow("video_receive_sample", image)
        cv2.waitKey(1)

