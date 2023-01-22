import sys
from Utils.Config import config
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import whisper
import opencc
import numpy as np
import pyaudio
import queue
import torch
torch.hub._validate_not_a_forked_repo = lambda a, b, c: True

class Translation(QThread):
    text = pyqtSignal(list)
    def __init__(self, recordType = 0, gap = 8000):
        super(Translation,self).__init__()

         # 创建队列用于存储录音数据
        self.q = queue.Queue()
        self.alldata = np.array([],np.float32)
        self.temp = np.array([],np.float32)
        self.LastEndD = 0
        self.Recording = False

        self.isRecord = False
        self.gap = gap

        # 定义录音类型和设备
        self.p = pyaudio.PyAudio()
        self.input_device_index = None
        if recordType != 0:
            for i in range(self.p.get_device_count()):
                dev = self.p.get_device_info_by_index(i)
                if '立体声混音' in dev['name']:
                    self.input_device_index = i
                    break
        self.stream = self.p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    input_device_index = self.input_device_index,
                    frames_per_buffer=1024,
                    stream_callback=self.recording_callback)

        # 加载whisper模型和语音定位模型
        self.cc = opencc.OpenCC('t2s')
        self.model = whisper.load_model(config["Translation"]["modelType"])
        self.options = whisper.DecodingOptions(language='zh')

        self.vad_model, funcs = torch.hub.load(
                    repo_or_dir="snakers4/silero-vad", model="silero_vad", trust_repo=True
                )
        self.detect_speech = funcs[0]

        self.stop()
        self.terminate()
    
    def run(self):
        self.record()

    def detect_voice_activity(self,audio):
            speeches = self.detect_speech(audio, self.vad_model, sampling_rate=16000)
            if len(speeches) == 2:
                if speeches[1]['start'] - speeches[0]['end'] < self.gap:
                    return [{"start": speeches[0]['start'], "end": speeches[1]['end']}]
            return speeches

    def get_audio_text(self,audio_data):
        audio = whisper.pad_or_trim(audio_data)
        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
        result = whisper.decode(self.model, mel, self.options)
        text = self.cc.convert(result.text)
        self.text.emit(["success!",text])
        print(text)

    def recording_callback(self,in_data, frame_count, time_info, status):
        # 将录制的数据存入队列
        self.q.put(in_data)
        return (in_data, pyaudio.paContinue)

    def record(self):
        # 开始录音
        self.stream.start_stream()
        self.isRecord = True

        while self.isRecord:
            data = b''
            while len(data) < 2*16000*2:
                data += self.q.get()
            self.temp = np.concatenate((self.temp, np.frombuffer(data, np.int16).flatten().astype(np.float32) / 32768.0), axis=0)
            speeches = self.detect_voice_activity(self.temp)
            if len(speeches) == 0:
                if self.Recording:
                    self.Recording = False
                    self.alldata = np.concatenate((self.alldata,self.temp), axis=0)
                    self.get_audio_text(self.alldata)
                self.alldata = np.array([],np.float32)
                self.temp = np.array([],np.float32)
                self.LastEndD = 0
            elif len(speeches) == 1:
                self.Recording = True
                start = int(speeches[0]['start'])
                end = int(speeches[0]['end'])

                if start + self.LastEndD < self.gap:
                    # 这是一句话
                    self.alldata = np.concatenate((self.alldata,self.temp[:end]), axis=0)
                    self.temp = self.temp[end:]
                    self.get_audio_text(self.alldata)
                    self.LastEndD = len(self.temp) - end
                else:
                    # 这是两句话
                    self.alldata = self.temp[:end]
                    self.temp = self.temp[end:]
                    self.get_audio_text(self.alldata)
                    self.LastEndD = len(self.temp) - end
            else:
                self.Recording = True
                self.temp = self.alldata[int(speeches[0]['end']):]
                self.alldata = self.alldata[:int(speeches[0]['end'])]
                self.get_audio_text(self.alldata)
                self.alldata = np.array([],np.float32)
                self.LastEndD = 0
            
    def stop(self):     #重写stop方法
        self.stream.stop_stream()
        self.isRecord = False