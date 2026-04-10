import json


def load_vulnerabilities(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_text(text):
    return text.lower().strip()


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

        # Exact alias match
        if query in aliases:
            score += 3

        # Exact text containment
        if query in searchable_text:
            score += 2

        # Token overlap
        score += token_overlap_score(query, searchable_text)

        if score > 0:
            results.append((score, vuln))

    results.sort(reverse=True, key=lambda x: x[0])
    return results[:3]


def main():
    file_path = "data/vulns.json"
    vulnerabilities = load_vulnerabilities(file_path)

    print("AI Security RAG Lab")
    user_query = input("Search vulnerability: ").strip()

    results = search_vulnerabilities(user_query, vulnerabilities)

    if results:
        print("\nTop Results:")
        for score, vuln in results:
            print(f"- ({score:.2f}) {vuln['name']}: {vuln['description']}")
    else:
        print("\nNo matching vulnerabilities found.")


if __name__ == "__main__":
    main()
