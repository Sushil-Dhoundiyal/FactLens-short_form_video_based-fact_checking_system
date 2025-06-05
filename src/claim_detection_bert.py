
import torch
from transformers import BertTokenizer, BertForMaskedLM
import re
import json
import os

def is_valid_sentence(sentence):
    """Filter out malformed, short, or gibberish sentences."""
    # Remove non-ASCII characters
    sentence = re.sub(r'[^\x00-\x7F]+',' ', sentence)

    # Basic rules for filtering
    if len(sentence.split()) < 5:
        return False
    if sentence.lower().startswith(('um', 'uh', 'okay', 'so')):
        return False
    if re.search(r'\d{2,}%|\b(?:yada|blah|gibberish)\b', sentence.lower()):
        return False
    if len(re.findall(r'\w+', sentence)) < 5:
        return False
    if sentence.count(',') > 4 or sentence.count('_') > 2:
        return False

    return True

def detect_claims(transcript_path, output_path):
    print("[2] Starting claim detection...")

    # Load BERT
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertForMaskedLM.from_pretrained("bert-base-uncased")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    print(f"Device set to use {device}")

    # Read transcript
    with open(transcript_path, 'r', encoding='utf-8') as f:
        transcript = f.read()

    # Split into candidate sentences
    sentences = re.split(r'[.?!]\s+', transcript.strip())
    detected_claims = []

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        # Simple confidence proxy: try masking random word and evaluating
        words = sentence.split()
        if len(words) < 5:
            continue

        masked_index = len(words) // 2
        masked_sentence = words.copy()
        masked_sentence[masked_index] = '[MASK]'
        masked_sentence = ' '.join(masked_sentence)

        inputs = tokenizer(masked_sentence, return_tensors='pt').to(device)
        with torch.no_grad():
            outputs = model(**inputs)
            predictions = outputs.logits

        # Calculate pseudo-confidence of masked word
        mask_token_index = (inputs.input_ids == tokenizer.mask_token_id).nonzero(as_tuple=True)[1]
        predicted_token_id = predictions[0, mask_token_index, :].argmax(dim=-1)
        predicted_token = tokenizer.decode(predicted_token_id)

        # You can use logit confidence or just keep all for now
        detected_claims.append(sentence)

    # Filter gibberish
    cleaned_claims = [claim for claim in detected_claims if is_valid_sentence(claim)]

    # Save results
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump([{"claim": c} for c in cleaned_claims], f, indent=2, ensure_ascii=False)

    print(f"{len(cleaned_claims)} claims detected and saved to {output_path}.")

