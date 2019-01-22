import lib.my_udp as udp
import lib.network_data as ip
from lib.audio_operator import AudioOperator


# udpで受け取るコールバック関数
#def call_my_udp_receive(data, record_flag, my_udp_receiver):
#    for data in receiver.receive():

def audio_receive(IP):
    port = udp.PORT_AUDIO
    receiver = udp.Receiver(IP, port)
    operator = AudioOperator(in_flag=False)
    # 音声を取り続ける
    for data in receiver.receive():
        operator.play(data)

    receiver.close()


if __name__ == "__main__":
    IP = ip.mac_pro_IP
    audio_receive(IP)

