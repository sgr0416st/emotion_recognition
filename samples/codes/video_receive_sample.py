import lib.my_udp as udp
import cv2


def video_receive(IP):
    port = udp.PORT_VIDEO
    receiver = udp.Receiver(IP, port)
    # 画像を取り続ける
    for img in receiver.receive_image():
        # 送信された画像の処理を行う
        cv2.imshow("video_receive_sample", img)
        # Enterキーで終了
        if cv2.waitKey(10) == 13:
            break

    receiver.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    IP = '127.0.0.1'
    video_receive(IP)


