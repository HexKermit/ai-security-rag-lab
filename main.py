from difflib import SequenceMatcher


def load_vulnerabilities(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines() if line.strip()]


def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def search_vulnerabilities(query, vulnerabilities, threshold=0.2):
    scored_results = []

    for vuln in vulnerabilities:
        score = similarity(query, vuln)
        if score >= threshold:
            scored_results.append((score, vuln))

    scored_results.sort(reverse=True, key=lambda x: x[0])
    return scored_results[:3]


def main():
    file_path = "data/vulns.txt"
    vulnerabilities = load_vulnerabilities(file_path)

    print("AI Security RAG Lab")
    user_query = input("Search vulnerability: ").strip()

    results = search_vulnerabilities(user_query, vulnerabilities)

    if results:
        print("\nTop Results:")
        for score, result in results:
            print(f"- ({score:.2f}) {result}")
    else:
        print("\nNo similar vulnerabilities found.")


if __name__ == "__main__":
    main()
