from src.loader import load_vulnerabilities
from src.semantic_search import semantic_search


def main():
    file_path = "data/vulns.json"
    vulnerabilities = load_vulnerabilities(file_path)

    print("AI Security RAG Lab")
    user_query = input("Search vulnerability: ").strip()

    results = semantic_search(user_query, vulnerabilities)

    if results:
        print("\nTop Results:")
        for score, vuln in results:
            print(f"- ({score:.4f}) {vuln['name']}: {vuln['description']}")
    else:
        print("\nNo matching vulnerabilities found.")


if __name__ == "__main__":
    main()
