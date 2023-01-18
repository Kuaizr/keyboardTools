from transformers import WhisperProcessor, WhisperForConditionalGeneration
import ffmpeg
import numpy as np
import datasets.features.audio
import torch


def load_audio(file: str, sr: int = 16000):
    try:
        out, _ = (
            ffmpeg.input(file, threads=0)
            .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=sr)
            .run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

# load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")

# load dummy dataset and read soundfiles
ds = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean", split="validation")
input_features = processor(ds[0]["audio"]["array"], return_tensors="pt").input_features 

# Generate logits
logits = model(input_features, decoder_input_ids = torch.tensor([[50258]])).logits 
# take argmax and decode
predicted_ids = torch.argmax(logits, dim=-1)
transcription = processor.batch_decode(predicted_ids)