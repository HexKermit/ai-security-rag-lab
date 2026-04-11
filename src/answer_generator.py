def generate_answer(query, top_vuln):
    name = top_vuln["name"]
    type_ = top_vuln.get("type", "unknown")
    description = top_vuln["description"]
    mitigation = top_vuln.get("mitigation", "No mitigation available.")
    aliases = ", ".join(top_vuln["aliases"])

    answer = []

    answer.append(f"\nAI Security Insight for '{query}':\n")
    answer.append(f"{name} is the most relevant result for your query.")

    answer.append("\nType:")
    answer.append(type_)

    answer.append("\nWhat it is:")
    answer.append(description)

    answer.append("\nWhy it matters:")

    if type_ == "vulnerability":
        answer.append(
            "This vulnerability can be abused by attackers to bypass protections, access sensitive data, or compromise application behavior."
        )
    elif type_ == "attack":
        answer.append(
            "This attack pattern matters because it describes how an attacker can exploit weaknesses in a real-world offensive scenario."
        )
    elif type_ == "technique":
        answer.append(
            "This technique matters because it is used by security testers and researchers to discover weaknesses in systems and applications."
        )
    elif type_ == "topic":
        answer.append(
            "This topic matters because it represents an important area of security knowledge that supports deeper understanding, testing, and defense."
        )
    else:
        answer.append(
            "This result is security-relevant and may help explain the user's query."
        )

    answer.append("\nCommon aliases:")
    answer.append(aliases)

    answer.append("\nBasic mitigation / handling:")
    answer.append(mitigation)

    return "\n".join(answer)
