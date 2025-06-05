
# from src.pipeline import process_video
# from src.fact_checker import verify_claims

# VIDEO_PATH = "data/test_video.mp4"
# CLAIMS_OUTPUT = "outputs/claims.json"
# VERIFIED_OUTPUT = "outputs/verified_claims.json"

# if __name__ == "__main__":
#     print("[1] Starting pipeline: extracting and detecting claims...")
#     process_video(VIDEO_PATH)

#     print(f"[2] Claim detection complete. Claims saved to {CLAIMS_OUTPUT}")

#     print("[3] Starting claim verification...")
#     verify_claims(claims_path=CLAIMS_OUTPUT, output_path=VERIFIED_OUTPUT)

#     print(f"[4] Verification complete. Verified results saved to {VERIFIED_OUTPUT}")



# to use with perplexity_fact_checker.py
from src.pipeline import process_video

VIDEO_PATH = "data/test_video.mp4"

if __name__ == "__main__":
        # print("[1] Starting pipeline: (audio extraction and Perplexity fact-checking ...")

    print("[1] Starting pipeline: (audio extraction........... transcription.......")
    process_video(VIDEO_PATH)

    print("[✔] Pipeline complete.")
