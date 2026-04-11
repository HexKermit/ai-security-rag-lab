from src.loader import load_vulnerabilities
from src.search import lexical_score
from src.semantic_search import semantic_scores


def format_answer(query, results):
    top_score, top_vuln = results[0]

    answer = []
    answer.append(f"\nBest Match for '{query}':")
    answer.append(f"- {top_vuln['name']}")
    answer.append(f"- Description: {top_vuln['description']}")
    answer.append(f"- Aliases: {', '.join(top_vuln['aliases'])}")
    answer.append(f"- Confidence Score: {top_score:.4f}")

    if len(results) > 1:
        answer.append("\nOther Possible Matches:")
        for score, vuln in results[1:]:
            answer.append(f"- {vuln['name']} ({score:.4f})")

    return "\n".join(answer)


def main():
    file_path = "data/vulns.json"
    vulnerabilities = load_vulnerabilities(file_path)

    print("AI Security RAG Lab")
    user_query = input("Search vulnerability: ").strip()

    semantic = semantic_scores(user_query, vulnerabilities)

    combined_results = []
    for i, vuln in enumerate(vulnerabilities):
        lex_score = lexical_score(user_query, vuln)
        sem_score = semantic[i]

        final_score = lex_score + sem_score
        combined_results.append((final_score, vuln))

    combined_results.sort(key=lambda x: x[0], reverse=True)
    top_results = combined_results[:3]

    print(format_answer(user_query, top_results))


if __name__ == "__main__":
    main()
