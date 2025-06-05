

def format_evidence(claim, evidence_sources):
    formatted = {
        "claim": claim,
        "evidence": [],
    }

    for source in evidence_sources:
        if source and "text" in source:
            formatted["evidence"].append({
                "source_type": source.get("source", "Unknown"),
                "content": source["text"],
                "source_url": source.get("url", "https://www.google.com/search?q=" + claim.replace(" ", "+"))
            })

    return formatted
