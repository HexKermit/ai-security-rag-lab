from src.loader import load_vulnerabilities
from src.search import lexical_score, normalize_text
from src.semantic_search import semantic_scores, prepare_documents
from src.answer_generator import generate_answer

STRONG_THRESHOLD = 4.0
WEAK_THRESHOLD = 1.5


def search(query, vulnerabilities, doc_embeddings):
    semantic = semantic_scores(query, doc_embeddings)
    query_lower = query.lower()

    results = []

    for i, vuln in enumerate(vulnerabilities):
        lex_score = lexical_score(query, vuln)
        sem_score = semantic[i]

        aliases = [a.lower() for a in vuln.get("aliases", [])]
        name_lower = vuln["name"].lower()

        # Exact match override
        if query_lower == name_lower or query_lower in aliases:
            final_score = 100.0
        else:
            final_score = lex_score + sem_score

        results.append((final_score, vuln))

    results.sort(key=lambda x: x[0], reverse=True)
    return results[:3]


def main():
    file_path = "data/vulns.json"
    vulnerabilities = load_vulnerabilities(file_path)

    print("Loading embeddings...")
    _, doc_embeddings = prepare_documents(vulnerabilities)

    print("\nAI Security RAG Lab")
    print("Type a query or 'exit' to quit.")

    while True:
        raw_query = input("\nSearch: ").strip()

        if raw_query.lower() == "exit":
            print("Goodbye.")
            break

        query = normalize_text(raw_query)

        if not query:
            print("Please enter a valid query.")
            continue

        results = search(query, vulnerabilities, doc_embeddings)
        top_score, top_vuln = results[0]

        if top_score < WEAK_THRESHOLD:
            print("\n[!] No strong match found.")
            print("Try a more specific query.\n")
            continue

        elif top_score < STRONG_THRESHOLD:
            print("\n[?] Did you mean:")
            for score, vuln in results:
                print(f"- {vuln['name']} ({score:.4f})")
            continue

        print("\n" + "=" * 50)
        print(generate_answer(raw_query, top_vuln))
        print(f"\nConfidence Score: {top_score:.4f}")

        if len(results) > 1:
            print("\nOther Matches:")
            for score, vuln in results[1:]:
                print(f"- {vuln['name']} ({score:.4f})")

        print("=" * 50)


if __name__ == "__main__":
    main()
