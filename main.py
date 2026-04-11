from src.loader import load_vulnerabilities
from src.search import lexical_score, normalize_text
from src.semantic_search import semantic_scores, prepare_documents
from src.answer_generator import generate_answer

DEBUG = False


def search_once(user_query, vulnerabilities, doc_embeddings):
    semantic = semantic_scores(user_query, doc_embeddings)

    combined_results = []
    for i, vuln in enumerate(vulnerabilities):
        lex_score = lexical_score(user_query, vuln)
        sem_score = semantic[i]
        final_score = lex_score + sem_score
        combined_results.append((final_score, vuln))

    combined_results.sort(key=lambda x: x[0], reverse=True)
    return combined_results[:3]


def main():
    file_path = "data/vulns.json"
    vulnerabilities = load_vulnerabilities(file_path)
    _, doc_embeddings = prepare_documents(vulnerabilities)

    print("AI Security RAG Lab")
    print("Type a query or 'exit' to quit.")

    while True:
        raw_query = input("\nSearch vulnerability: ").strip()

        if raw_query.lower() == "exit":
            print("Goodbye.")
            break

        user_query = normalize_text(raw_query)

        if not user_query:
            print("Please enter a valid query.")
            continue

        if DEBUG:
            print(f"[DEBUG] Raw input: {raw_query}")
            print(f"[DEBUG] Normalized input: {user_query}")

        results = search_once(user_query, vulnerabilities, doc_embeddings)
        top_score, top_vuln = results[0]

        print(generate_answer(user_query, top_vuln))
        print(f"\nConfidence Score: {top_score:.4f}")

        if len(results) > 1:
            print("\nOther Possible Matches:")
            for score, vuln in results[1:]:
                print(f"- {vuln['name']} ({score:.4f})")


if __name__ == "__main__":
    main()
