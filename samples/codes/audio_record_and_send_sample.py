import lib.my_udp as udp
import lib.network_data as ip
from lib.sota.command import Command
from lib.sota.request_sender import RequestSender
from lib.audio_operator import AudioOperator
import time
import numpy as np


class AudioSenderLists:
    def __init__(self, threshold, request_sender, udp_sender):
        self.threshold = threshold
        self.request_sender = request_sender
        self.udp_sender = udp_sender


# udpで送るコールバック関数
def call_my_udp_send(data, record_flag, my_udp_sender):
    my_udp_sender.send(data)


def call_audio_send_operator(data, record_flag, audio_send_operator):
    amp = np.fromstring(data, np.int16)
    max = amp.max()
    if max > audio_send_operator.threshold:
        audio_send_operator.request_sender.send()
        audio_send_operator.request_sender.clear()
        audio_send_operator.request_sender.set_request_header(Command.COM_TEST)
    audio_send_operator.udp_sender.send(data)


def audio_record_and_send(dst, IP):
    port = udp.PORT_AUDIO
    sender = udp.Sender(IP, port)
    operator = AudioOperator(out_flag=False, callback_func=call_my_udp_send, callback_func_data=sender)
    operator.record(dst)
    while operator.stream.is_active():
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            operator.stop()
            break

    operator.close()


def audio_record_and_send_with_sota(dst, send_IP):
    threshold = 6000
    sota_sender = RequestSender()
    sota_sender.connect(send_ip=Command.SOTA_IP)
    sota_sender.set_request_header(Command.COM_TEST)
    send_port = udp.PORT_AUDIO
    udp_sender = udp.Sender(send_IP, send_port)
    audio_sender_lists = AudioSenderLists(threshold, sota_sender, udp_sender)
    operator = AudioOperator(out_flag=False, callback_func=call_audio_send_operator, callback_func_data=audio_sender_lists)
    operator.record(dst)

    while operator.stream.is_active():
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            operator.stop()
            break

    operator.close()


if __name__ == "__main__":
    dst = "../datas/audio_record_and_send_sample_data/sample_audio_org.wav"
    IP = ip.mac_pro_IP
    audio_record_and_send(dst, IP)
