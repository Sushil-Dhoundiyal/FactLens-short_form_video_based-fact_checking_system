
import requests
import logging

# --- Google Fact Check ---
def query_google_fact_check_api(claim: str, api_key: str) -> list[dict]:
    try:
        url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
        params = {"query": claim, "key": api_key}
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json().get("claims", [])
        
        results = []
        for claim_item in data:
            reviews = claim_item.get("claimReview", [])
            if not reviews:
                continue
            for review in reviews:
                publisher = review.get("publisher", {}).get("site", "")
                textual_rating = review.get("textualRating", "")
                review_url = review.get("url", "")
                results.append({
                    "text": textual_rating or review.get("title", ""),
                    "url": review_url,
                    "source": publisher or "Google Fact Check"
                })
        return results

    except Exception as e:
        logging.error(f"Google Fact Check API error: {e}")
        return []

# --- NewsAPI ---
def query_newsapi(claim: str, api_key: str) -> list[dict]:
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": claim,
            "apiKey": api_key,
            "language": "en",
            "sortBy": "relevancy",
            "pageSize": 5
        }
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        articles = r.json().get("articles", [])
        
        results = []
        for a in articles:
            title = a.get("title", "")
            desc = a.get("description", "")
            full_text = f"{title}. {desc}" if desc else title
            results.append({
                "text": full_text,
                "url": a.get("url", ""),
                "source": a.get("source", {}).get("name", "NewsAPI")
            })
        return results

    except Exception as e:
        logging.error(f"NewsAPI error: {e}")
        return []

# --- Wikipedia ---
def query_wikipedia(claim: str) -> list[dict]:
    try:
        search_url = "https://en.wikipedia.org/w/api.php"
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": claim,
            "format": "json",
            "srlimit": 1
        }
        r = requests.get(search_url, params=search_params, timeout=10)
        r.raise_for_status()
        search_results = r.json().get("query", {}).get("search", [])
        if not search_results:
            return []

        title = search_results[0]["title"]
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title.replace(' ', '_')}"
        r2 = requests.get(summary_url, timeout=10)
        r2.raise_for_status()
        summary_data = r2.json()

        extract = summary_data.get("extract", "")
        page_url = summary_data.get("content_urls", {}).get("desktop", {}).get("page", "")

        return [{
            "text": extract,
            "url": page_url,
            "source": "Wikipedia"
        }]

    except Exception as e:
        logging.error(f"Wikipedia error: {e}")
        return []

# --- Combined fetcher ---
def fetch_fact_check_data(claim: str, google_key: str, newsapi_key: str) -> list[dict]:
    results = []
    results.extend(query_google_fact_check_api(claim, google_key))
    results.extend(query_newsapi(claim, newsapi_key))
    results.extend(query_wikipedia(claim))
    return results
