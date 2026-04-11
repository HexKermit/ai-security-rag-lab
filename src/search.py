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
        return 0.0

    overlap = query_tokens.intersection(text_tokens)
    return len(overlap) / len(query_tokens)


def lexical_score(query, vuln):
    query = normalize_text(query)

    name = vuln["name"]
    aliases = [normalize_text(alias) for alias in vuln["aliases"]]
    description = vuln["description"]

    searchable_text = normalize_text(" ".join([name] + aliases + [description]))

    score = 0.0

    if query in aliases:
        score += 3.0

    if query in searchable_text:
        score += 2.0

    score += token_overlap_score(query, searchable_text)

    return score
