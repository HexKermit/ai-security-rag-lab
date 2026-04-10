def load_vulnerabilities(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.readlines()


def search_vulnerabilities(query, vulnerabilities):
    query = query.lower().strip()
    results = []

    for vuln in vulnerabilities:
        if query in vuln.lower():
            results.append(vuln.strip())

    return results


def main():
    file_path = "data/vulns.txt"
    vulnerabilities = load_vulnerabilities(file_path)

    print("AI Security RAG Lab")
    user_query = input("Search vulnerability: ")

    results = search_vulnerabilities(user_query, vulnerabilities)

    if results:
        print("\nResults:")
        for result in results:
            print(f"- {result}")
    else:
        print("\nNo matching vulnerabilities found.")


if __name__ == "__main__":
    main()
