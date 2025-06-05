

from sentence_transformers import SentenceTransformer, util
import torch

# Upgraded to more accurate model
model = SentenceTransformer("all-mpnet-base-v2")

# Thresholds
HIGH_CONFIDENCE = 0.55
MID_CONFIDENCE = 0.40
TOP_K = 3  # Number of top sources to return

def check_similarity(claim_text, fact_data):
    """
    Compare a claim text with a list of fact entries to determine semantic similarity.

    Returns:
        Tuple[str, list]: Verdict ("Likely True", "Possibly True", or "Likely False") and matched sources.
    """
    if not fact_data:
        return "Unverifiable", []

    # Encode the claim
    claim_embedding = model.encode(claim_text, convert_to_tensor=True)

    # Encode all fact entries
    fact_texts = [entry["text"] for entry in fact_data]
    fact_embeddings = model.encode(fact_texts, convert_to_tensor=True)

    # Compute cosine similarity scores
    cosine_scores = util.pytorch_cos_sim(claim_embedding, fact_embeddings)[0]

    # Rank top matches
    top_results = sorted(
        zip(cosine_scores, fact_data),
        key=lambda x: x[0],
        reverse=True
    )[:TOP_K]

    matched_sources = []
    strong_match = False

    for score, entry in top_results:
        score_value = score.item()
        if score_value >= MID_CONFIDENCE:
            matched_sources.append(entry["source"])
        if score_value >= HIGH_CONFIDENCE:
            strong_match = True

    if strong_match:
        verdict = "Likely True"
    elif matched_sources:
        verdict = "Possibly True"
    else:
        # Fallback keyword-based partial match
        claim_keywords = set(claim_text.lower().split())
        for entry in fact_data:
            evidence_keywords = set(entry["text"].lower().split())
            if claim_keywords & evidence_keywords:
                return "Unverifiable", [entry["source"]]

        verdict = "Likely False"

    return verdict, matched_sources
