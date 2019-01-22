from samples.codes.audio_record_and_send_sample import audio_record_and_send
from samples.codes.audio_record_and_send_sample import audio_record_and_send_with_sota
from samples.codes.video_record_and_send_sample import video_record_and_send
import threading
import lib.network_data as ip

if __name__ == "__main__":
    dst_video = "../datas/video_audio_record_send_sample_data/sample_video_org.avi"
    dst_audio = "../datas/video_audio_record_send_sample_data/sample_audio_org.wav"
    receive_IP = ip.mac_pro_IP
    send_IP = ip.mac_IP

    thread_video_rec = threading.Thread(target=video_record_and_send, args=([dst_video, send_IP]))
    thread_audio_rec = threading.Thread(target=audio_record_and_send_with_sota, args=([dst_audio, send_IP]))

    thread_video_rec.start()
    thread_audio_rec.start()

    thread_video_rec.join()
    thread_audio_rec.join()
