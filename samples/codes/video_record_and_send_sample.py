import lib.my_udp as udp
from lib.video_operater import VideoOperator


# udpで送るコールバック関数
def call_my_udp_send_image(frame, my_udp_sender):
    my_udp_sender.send_image(frame)


def video_record_and_send(dst, IP):
    port = udp.PORT_VIDEO
    sender = udp.Sender(IP, port)
    operator = VideoOperator()
    callback = call_my_udp_send_image
    operator.record(dst, func=callback, func_data=sender)
    operator.close()


def video_slice(dst, dst_slice):
    operator_2 = VideoOperator(org_path=dst)
    operator_2.record(dst_slice, record_fps=1)
    operator_2.close()


if __name__ == "__main__":
    dst = "../datas/video_record_and_send_sample_data/sample_video_org.avi"
    IP = '127.0.0.1'
    dst_slice = "sample_datas/video_record_and_send_sample_data/video_sample_slice.avi"
    video_record_and_send(dst, IP)
    video_slice(dst, dst_slice)
