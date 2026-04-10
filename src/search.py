import re


def normalize_text(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def token_overlap_score(query, text):
    query_tokens = set(normalize_text(query).split())
    text_tokens = set(normalize_text(text).split())

    if not query_tokens or not text_tokens:
        return 0

    overlap = query_tokens.intersection(text_tokens)
    return len(overlap) / len(query_tokens)


def search_vulnerabilities(query, vulnerabilities):
    query = normalize_text(query)
    results = []

    for vuln in vulnerabilities:
        name = vuln["name"]
        aliases = vuln["aliases"]
        description = vuln["description"]

        searchable_text = " ".join([name] + aliases + [description]).lower()

        score = 0

        if query in aliases:
            score += 3

        if query in searchable_text:
            score += 2

        score += token_overlap_score(query, searchable_text)

        if score > 0:
            results.append((score, vuln))

    results.sort(reverse=True, key=lambda x: x[0])
    return results[:3]
