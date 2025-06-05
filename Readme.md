# 🔍 FactLens – AI-Based Short Video Fact Checker

**FactLens** is a robust end-to-end AI system that **detects and verifies factual claims** from short videos like Instagram Reels or YouTube Shorts. It combines speech recognition, natural language processing, semantic similarity, and real-time API querying to verify information shared in videos.

---

## 🚀 Key Features

- 🎥 Extracts audio from short videos (Reels, Shorts, etc.)
- 🧠 Transcribes audio using OpenAI Whisper
- ✅ Detects factual claims using BERT-based classification
- 🔎 Verifies claims using:
  - Wikipedia
  - Google Fact Check API
  - NewsAPI
- 🔗 Uses MiniLM for semantic similarity between claims and sources
- 🌐 Flask backend for web-based uploads and result display

---

## 🔄 Project Workflow

          User Uploads Video (Frontend)
                     |
                 [Flask App]
                     |
          ┌────────────────────────┐
          │  1. Audio Extraction    │ ← 🎥 `audio_extraction.py`
          │  2. Speech-to-Text     │ ← 🧠 `speech_to_text.py`
          │  3. Claim Detection    │ ← 🤖 `claim_detection_bert.py`
          │  4. Fact Verification  │ ← 🔎 `fact_checker.py`
          │  5. Output Results     │ ← 📁 `verified_claims.json`
          └────────────────────────┘
                     ↓
            Results Shown in Browser

---

## ⚙️ Setup Instructions

1. Set Up Virtual Environment (Optional but Recommended)
   python -m venv venv
   source venv/bin/activate # Windows: venv\Scripts\activate

📦 Install Dependencies
   pip install -r requirements.txt

2. (Optional) Install ffmpeg (Required by moviepy & pydub)
   Make sure ffmpeg is installed and added to your PATH.
   Install from: https://ffmpeg.org/download.html

3. 🌐 Run Web Interface (Flask)
   python app.py

4. From the browser:
   Upload a short video
   Click "Fact Check"
   View claim verification results

## Output Screenshots
![Screenshot (39)](https://github.com/user-attachments/assets/546b0dd0-8e5b-43ad-9620-076272eaafdf)

![Screenshot (40)](https://github.com/user-attachments/assets/f27864f8-4bba-444d-a772-85899da1642c)

![Screenshot (42)](https://github.com/user-attachments/assets/f3ca4afd-e5d3-4993-b2b9-380cb6002247)
![Screenshot (43)](https://github.com/user-attachments/assets/0ed6fbb1-71ee-48db-9587-932aaeaec9a5)

![Screenshot (44)](https://github.com/user-attachments/assets/b58cecb5-d602-4103-8b3b-45271f796ccd)




