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

🧾 Sample Output (verified_claims.json)
[
{
"claim": "The Taj Mahal was built in 1632.",
"verdict": "True",
"source": ["https://en.wikipedia.org/wiki/Taj_Mahal"],
"explanation": "Multiple historical records confirm the construction of the Taj Mahal began in 1632."
},
{
"claim": "Vaccines cause autism.",
"verdict": "False",
"source": ["https://www.cdc.gov/vaccinesafety/concerns/autism.html"],
"explanation": "No credible scientific evidence supports the claim that vaccines cause autism."
}
]
