import pyaudio
import wave


class AudioOperator:
    def __init__(self, in_flag=True, out_flag=True, chunk=4096, audio_format=pyaudio.paInt16, channels=1, rate=44100,
                 callback_func=None, callback_func_data=None):
        self.in_flag=in_flag
        self.out_flag=out_flag
        self.chunk = chunk
        self.audio_format = audio_format
        self.channels = channels
        self.rate = rate
        self.wf = None
        self.record_flag = False
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.callback_func = callback_func
        self.callback_func_data = callback_func_data
        self.open()

    def callback(self, in_data, frame_count, time_info, status):
        data = in_data
        if self.record_flag is True:
            self.wf.writeframes(in_data)
        if self.callback_func is not None:
            data = self.callback_func(in_data, self.record_flag, self.callback_func_data)
        out_data = data
        return out_data, pyaudio.paContinue

    # ストリームを開く
    def open(self):
        f = None
        if self.callback_func is not None:
            f = self.callback
        self.stream = self.p.open(format=self.audio_format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  input=self.in_flag,
                                  output=self.out_flag,
                                  frames_per_buffer=self.chunk,
                                  stream_callback=f
                                  )
        self.stream.start_stream()

    # 新しい音声ファイルを作成し、録音を開始する
    def record(self, audio_path):
        self.wf = wave.open(audio_path, 'wb')
        self.wf.setnchannels(self.channels)
        self.wf.setsampwidth(self.p.get_sample_size(self.audio_format))
        self.wf.setframerate(self.rate)
        self.record_flag = True

    # 中断された録音を再開する
    def restart(self):
        self.record_flag = True

    # 現在の録音を中断する。
    def halt(self):
        self.record_flag = False

    # 現在の録音を終了し、音声ファイルを閉じる
    def stop(self):
        self.record_flag = False
        self.wf.close()
        self.wf = None

    def play(self, data):
        self.stream.write(data)

    # ストリームを閉じて終了する
    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
