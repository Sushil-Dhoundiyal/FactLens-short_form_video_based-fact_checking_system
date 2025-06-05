
# import os 
# from src.audio_extraction import extract_audio
# from src.speech_to_text import transcribe_audio
# from src.claim_detection_bert import detect_claims

# DATA_DIR = "data"
# OUTPUT_DIR = "outputs"

# def process_video(video_path):
#     audio_path = os.path.join(DATA_DIR, "extracted_audio.mp3")
#     transcript_path = os.path.join(OUTPUT_DIR, "transcript.txt")
#     claims_path = os.path.join(OUTPUT_DIR, "claims.json")

#     # Step 1: Extract audio
#     extract_audio(video_path, audio_path)

#     # Step 2: Transcribe
#     transcript = transcribe_audio(audio_path, transcript_path)

#     # Step 3: Claim detection and save directly
#     detect_claims(transcript_path, claims_path)

#     print(f"Claims saved to: {claims_path}")



# to use with perplexity_fact_checker.py
import os 
from src.audio_extraction import extract_audio
from src.speech_to_text import transcribe_audio
from src.perplexity_fact_checker import fact_check_with_sonar

DATA_DIR = "data"
OUTPUT_DIR = "outputs"

def process_video(video_path):
    audio_path = os.path.join(DATA_DIR, "extracted_audio.mp3")
    transcript_path = os.path.join(OUTPUT_DIR, "transcript.txt")
    verified_output_path = os.path.join(OUTPUT_DIR, "verified_claims.json")

    # Step 1: Extract audio
    extract_audio(video_path, audio_path)

    # Step 2: Transcribe audio
    print("Audio transcribing...............")
    transcribe_audio(audio_path, transcript_path)

    # Step 3: Fact-check using perplexity
    print("Checking authenticity of the facts...........")
    fact_check_with_sonar(transcript_path, verified_output_path)

    print(f"[✅] Verified results saved to: {verified_output_path}")
