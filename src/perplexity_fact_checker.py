# Fallback script to handle claim detection and verification



import requests
import json
from src.config import PERPLEXITY_API_KEY  # Ensure your config is correct

# Load API Key and Endpoint
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {PERPLEXITY_API_KEY}"
}
SONAR_API_URL = "https://api.perplexity.ai/chat/completions"


def fact_check_with_sonar(transcript_path, output_path):
    with open(transcript_path, 'r', encoding='utf-8') as f:
        transcript = f.read()

    # Improved Prompt with real URLs and clickable source request
    prompt = f"""
You are a reliable, research-based fact-checking assistant.

Your task is to:
1. Detect factual claims from the transcript below.
2. For each claim, determine if it is True, False, Partially True, or Unverified.
3. Always attempt to find at least one real source (preferably news, academic, or government).
4. If no credible source is found after careful checking, mark it as "Unverified", but only as a last resort.
5. Never omit the source field – always return an empty list ([]) if no sources exist.

**Format requirements** (strict JSON):
- "claim": the factual statement
- "verdict": one of ["True", "False", "Partially True", "Unverified"]
- "source": list of valid and real URLs only — no placeholders or citations like [1]
- "explanation": 2–4 sentences explaining the verdict based on the source(s)

Here is the transcript to analyze:
\"\"\"{transcript}\"\"\"

Respond only with a JSON array as below:
[
  {{
    "claim": "...",
    "verdict": "...",
    "source": ["https://example.com"],
    "explanation": "..."
  }},
  ...
]
"""


    payload = {
        "model": "sonar",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 1500
    }

    response = requests.post(SONAR_API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        print(f"[ERROR] Sonar API request failed: {response.status_code} {response.text}")
        return

    try:
        data = response.json()
        content = data['choices'][0]['message']['content']
        claims = json.loads(content)
    except Exception as e:
        print(f"[ERROR] Failed to parse Sonar API response: {e}")
        claims = []

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(claims, f, indent=2, ensure_ascii=False)
