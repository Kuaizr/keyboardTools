import whisper
import opencc
cc = opencc.OpenCC('t2s')
model = whisper.load_model("base")
audio = whisper.load_audio("out.mp3")
audio = whisper.pad_or_trim(audio)

mel = whisper.log_mel_spectrogram(audio).to(model.device)

options = whisper.DecodingOptions()
result = whisper.decode(model, mel, options)

print(cc.convert(result.text))