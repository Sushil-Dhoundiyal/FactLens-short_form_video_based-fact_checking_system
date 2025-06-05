

import torch
from transformers import pipeline as hf_pipeline

def transcribe_audio(audio_path, transcript_path):
    print("🔠 Transcribing audio to English...")

    # Use GPU if available
    device = 0 if torch.cuda.is_available() else -1

    # Use multilingual Whisper model with translation to English
    whisper = hf_pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-small",  # or "whisper-medium", "whisper-large"
        device=device,
        generate_kwargs={"task": "translate"},  # ensures English output
        return_timestamps=True          # to handle large video(> 1 min )
    )

    print("🔠 Transcribing audio to English...")
    result = whisper(audio_path)
    transcript = result["text"]

    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript)

    print("📝 Transcription complete and saved to", transcript_path)
    return transcript_path
