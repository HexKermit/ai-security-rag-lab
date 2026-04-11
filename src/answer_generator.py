def generate_answer(query, top_vuln):
    name = top_vuln["name"]
    description = top_vuln["description"]
    mitigation = top_vuln.get("mitigation", "No mitigation available.")
    aliases = ", ".join(top_vuln["aliases"])

    answer = []

    answer.append(f"\nAI Security Insight for '{query}':\n")
    answer.append(f"{name} is the most relevant vulnerability for your query.")

    answer.append("\nWhat it is:")
    answer.append(description)

    answer.append("\nWhy it matters:")
    answer.append(
        "This type of vulnerability can be exploited by attackers to compromise system security, "
        "steal data, or execute malicious actions."
    )

    answer.append("\nCommon aliases:")
    answer.append(aliases)

    answer.append("\nBasic mitigation:")
    answer.append(mitigation)

    return "\n".join(answer)
