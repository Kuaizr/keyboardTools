import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import whisper
import opencc
import numpy as np
import pyaudio
import threading
import queue
import asyncio
import torch
torch.hub._validate_not_a_forked_repo = lambda a, b, c: True

class Translation(QThread):
    def __init__(self):
        super(Translation,self).__init__()

        self.cc = opencc.OpenCC('t2s')
        self.model = whisper.load_model("base")
        self.options = whisper.DecodingOptions(language='zh')

        
        self.vad_model, funcs = torch.hub.load(
                    repo_or_dir="snakers4/silero-vad", model="silero_vad", trust_repo=True
                )
        self.detect_speech = funcs[0]

        # 创建队列用于存储录音数据
        self.q = queue.Queue()
        self.alldata = np.array([],np.float32)
        self.temp = np.array([],np.float32)
    
    def run(self):
        while True:
            pass
    
    def detect_voice_activity(self,audio):
            speeches = self.detect_speech(audio, self.vad_model, sampling_rate=16000)
            return speeches if len(speeches) > 1 else [{"start": 0, "end": len(audio)}]

    def get_audio_text(self,audio_data):
        audio = whisper.pad_or_trim(audio_data)
        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
        result = whisper.decode(self.model, mel, self.options)
        print(self.cc.convert(result.text))

    def recording_callback(self,in_data, frame_count, time_info, status):
        # 将录制的数据存入队列
        self.q.put(in_data)
        return (in_data, pyaudio.paContinue)


    async def process(self,data):
        self.temp = np.concatenate((self.temp, np.frombuffer(data, np.int16).flatten().astype(np.float32) / 32768.0), axis=0)
        self.alldata = np.concatenate((self.alldata,self.temp), axis=0)
        speeches = self.detect_voice_activity(self.alldata)
        if len(speeches) == 1:
            print(1)
            self.get_audio_text(self.alldata)
            self.temp = np.array([],np.float32)
        else:
            print(2)
            self.temp = self.alldata[int(speeches[0]['end']):]
            self.alldata = self.alldata[int(speeches[0]['start']):int(speeches[0]['end'])]
            self.get_audio_text(self.alldata)
            self.alldata = np.array([],np.float32)


    async def record(self):
        self.p = pyaudio.PyAudio()
        # 打开麦克风输入流
        self.stream = self.p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=1024,
                        stream_callback=self.recording_callback)
        # 开始录音
        self.stream.start_stream()

        while True:
            data = b''
            while len(data) < 2*16000*2:
                data += self.q.get()
            await self.process(data)
        

    # # 停止录音
    # stream.stop_stream()
    # stream.close()

# 开启录音线程
# t = threading.Thread(target=record)
# t.start()

if __name__ == "__main__":
    application=QApplication(sys.argv)#窗口通讯
    a = Translation()
    a.start()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(a.record())
    sys.exit(application.exec_())