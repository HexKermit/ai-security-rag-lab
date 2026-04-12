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

        exact_match = query_lower == name_lower or query_lower in aliases

        if exact_match:
            final_score = 100.0
        else:
            final_score = lex_score + sem_score

        results.append(
            {
                "final_score": final_score,
                "lex_score": lex_score,
                "sem_score": sem_score,
                "exact_match": exact_match,
                "vuln": vuln,
            }
        )

    results.sort(key=lambda x: x["final_score"], reverse=True)
    return results[:3]


def build_confidence_explanation(top_result):
    if top_result["exact_match"]:
        return "Strong confidence because the query exactly matched the record name or one of its aliases."

    lex_score = top_result["lex_score"]
    sem_score = top_result["sem_score"]

    reasons = []

    if lex_score < 1.0:
        reasons.append("weak lexical match")
    else:
        reasons.append("reasonable lexical match")

    if sem_score < 0.8:
        reasons.append("weak semantic similarity")
    else:
        reasons.append("reasonable semantic similarity")

    return "Confidence explanation: " + ", ".join(reasons) + "."


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

        top_result = results[0]
        top_score = top_result["final_score"]
        top_vuln = top_result["vuln"]

        if top_score < WEAK_THRESHOLD:
            print("\n[!] No strong match found.")
            print("Try a more specific query.")
            print(build_confidence_explanation(top_result))
            continue

        elif top_score < STRONG_THRESHOLD:
            print("\n[?] Did you mean:")
            print(build_confidence_explanation(top_result))
            for result in results:
                vuln = result["vuln"]
                score = result["final_score"]
                print(f"- {vuln['name']} ({score:.4f})")
            continue

        print("\n" + "=" * 50)
        print(generate_answer(raw_query, top_vuln))
        print(f"\nConfidence Score: {top_score:.4f}")
        print(build_confidence_explanation(top_result))

        if len(results) > 1:
            print("\nOther Matches:")
            for result in results[1:]:
                vuln = result["vuln"]
                score = result["final_score"]
                print(f"- {vuln['name']} ({score:.4f})")

        print("=" * 50)


if __name__ == "__main__":
    main()
