import soundfile as sf
import librosa
import torch
import time
torch.hub._validate_not_a_forked_repo = lambda a, b, c: True
vad_model, funcs = torch.hub.load(
            repo_or_dir="snakers4/silero-vad", model="silero_vad", trust_repo=True
        )
detect_speech = funcs[0]

def detect_voice_activity(audio):
    speeches = detect_speech(audio, vad_model, sampling_rate=16000)
    return speeches if len(speeches) > 1 else [{"start": 0, "end": len(audio)}]

audio_data, _ = librosa.load("audio.wav", sr=16000)
tic = time.time()
print(detect_voice_activity(audio_data))
print(f"Done voice activity detection in {time.time() - tic} sec")

# sf.write('voice_1' + '.wav', audio_data[37408:77280], 16000)
# sf.write('voice_2' + '.wav', audio_data[101920:107488], 16000)