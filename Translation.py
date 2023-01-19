import whisper

model = whisper.load_model("base")
result = model.transcribe("out.mp3")
print(result["text"])