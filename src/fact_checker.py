

import json
from .config import GOOGLE_FACT_CHECK_API_KEY, NEWSAPI_KEY
from .api_clients import fetch_fact_check_data
from .similarity_matcher import check_similarity
from .evidence_formatter import format_evidence

def verify_claims(
    claims_path="outputs/claims.json",
    output_path="outputs/verified_claims.json"
):
    # 1) Load detected claims
    with open(claims_path, "r", encoding="utf-8") as f:
        claims = json.load(f)

    final_results = []

    for claim in claims:
        text = claim.get("text") or claim.get("claim") or ""
        text = text.strip()
        if not text:
            continue

        # 2) Fetch combined evidence from Google, NewsAPI, and Wikipedia
        fact_data = fetch_fact_check_data(
            claim=text,
            google_key=GOOGLE_FACT_CHECK_API_KEY,
            newsapi_key=NEWSAPI_KEY
        )
        # fact_data is now a list of dicts: [{ text, url, source }, ...]
        
        # 3) Compute similarity and verdict
        verdict, matched_sources = check_similarity(text, fact_data)
        # matched_sources is a list of the `source` strings that best matched

        # 4) Filter the matched entries for formatting
        matched_evidence = [
            entry for entry in fact_data
            if entry["source"] in matched_sources
        ]

        # 5) Format the output, including text, verdict, and evidence list
        result = format_evidence(text, matched_evidence)
        result["verdict"] = verdict or "No Data Found"

        final_results.append(result)

    # 6) Write out the verified claims
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_results, f, indent=4, ensure_ascii=False)

    print(f"Verified claims saved to: {output_path}")

