import pyaudio
import wave


CHUNK = 1024  # 音声処理をするときは2倍のサイズで
FORMAT = pyaudio.paInt16 # int16型
#CHANNELS = 2             # ステレオ
CHANNELS = 1          # マイクによってはモノラル
RATE = 44100             # 441.kHz
RECORD_SECONDS = 5       # 5秒録音
WAVE_OUTPUT_FILENAME = "/Users/satousuguru/workspace/programing/python/emotion_recognition/test_datas/output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int((RATE / CHUNK) * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

