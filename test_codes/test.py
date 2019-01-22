import threading
import lib.network_data as ip
import lib.my_udp as udp
from lib.audio_operator import AudioOperator
import time


# udpで送るコールバック関数
def call_my_udp_send(data, record_flag, my_udp_sender):
    my_udp_sender.send(data)


if __name__ == "__main__":
    dst_video = "../datas/video_audio_record_send_sample_data/sample_video_org.avi"
    dst_audio = "../datas/video_audio_record_send_sample_data/sample_audio_org.wav"
    receive_IP = ip.mac_pro_IP
    send_IP = ip.mac_IP
    audio_port = udp.PORT_AUDIO
    video_port = udp.PORT_VIDEO
    audio_sender = udp.Sender(send_IP, audio_port)
    video_sender = udp.Sender(send_IP, video_port)
    audio_receiver = udp.Receiver(receive_IP, audio_port)
    operator = AudioOperator(callback_func=call_my_udp_send, callback_func_data=audio_sender)


    def record_send_audio(dst, operator):
        operator.record(dst)
        while operator.stream.is_active():
            try:
                time.sleep(0.1)
            except KeyboardInterrupt:
                operator.stop()
                break

        operator.close()


    def recieve_audio(receiver, operator):
        for data in receiver.receive():
            operator.play(data)
        receiver.close()


    # thread_video_rec = threading.Thread(target=video_record_and_send, args=([dst_video, send_IP]))
    thread_audio_rec = threading.Thread(target=audio_record_and_send, args=([dst_audio, send_IP]))
    thread_audio_out = threading.Thread(target=audio_receive, args=([receive_IP]))

    # thread_video_rec.start()
    thread_audio_rec.start()
    thread_audio_out.start()

    # thread_video_rec.join()
    # thread_audio_rec.join()
    # thread_audio_out.join()
