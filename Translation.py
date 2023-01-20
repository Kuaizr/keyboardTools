import pyaudio
import threading
import queue

# 配置录音参数
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

import torch
torch.hub._validate_not_a_forked_repo = lambda a, b, c: True
vad_model, funcs = torch.hub.load(
            repo_or_dir="snakers4/silero-vad", model="silero_vad", trust_repo=True
        )
detect_speech = funcs[0]

import whisper
import opencc
import numpy as np
cc = opencc.OpenCC('t2s')
model = whisper.load_model("base")
options = whisper.DecodingOptions(language='zh')

def get_audio_text(audio_data):
    audio = whisper.pad_or_trim(audio_data)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    result = whisper.decode(model, mel, options)
    # print(cc.convert(result.text))
    print(result.text)


# 创建队列用于存储录音数据
q = queue.Queue()

def detect_voice_activity(audio):
    speeches = detect_speech(
        audio, vad_model, sampling_rate=16000
    )

    return speeches if len(speeches) > 1 else [{"start": 0, "end": len(audio)}]

def recording_callback(in_data, frame_count, time_info, status):
    # 将录制的数据存入队列
    q.put(in_data)
    return (in_data, pyaudio.paContinue)

def record():
    p = pyaudio.PyAudio()
    # 打开麦克风输入流
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    stream_callback=recording_callback)
    # 开始录音
    stream.start_stream()
    alldata = np.array([],np.float32)
    temp = np.array([],np.float32)
    data = b''
    while True:
        while len(data) < 2*RATE*2:
            data += q.get()
        temp = np.concatenate((temp, np.frombuffer(data, np.int16).flatten().astype(np.float32) / 32768.0), axis=0)
        alldata = np.concatenate((alldata,temp), axis=0)
        speeches = detect_voice_activity(alldata)
        if len(speeches) == 1:
            get_audio_text(alldata)
            data = b''
            temp = np.array([],np.float32)
        else:
            temp = alldata[int(speeches[0]['end']):]
            alldata = alldata[int(speeches[0]['start']):int(speeches[0]['end'])]
            data = b''
            get_audio_text(alldata)
            alldata = np.array([],np.float32)

    # 停止录音
    stream.stop_stream()
    stream.close()

# 开启录音线程
t = threading.Thread(target=record)
t.start()