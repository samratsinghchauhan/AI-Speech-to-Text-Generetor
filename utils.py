import torch
import soundfile as sf
import librosa
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

# Load Wav2Vec2 pre-trained model and tokenizer
tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

def preprocess_audio(file_path):
    audio, _ = librosa.load(file_path, sr=16000)
    sf.write("temp.wav", audio, 16000)
    return "temp.wav"

def transcribe(audio_path):
    audio_input, _ = sf.read(audio_path)
    input_values = tokenizer(audio_input, return_tensors="pt", padding="longest").input_values

    with torch.no_grad():
        logits = model(input_values).logits

    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = tokenizer.decode(predicted_ids[0])
    return transcription