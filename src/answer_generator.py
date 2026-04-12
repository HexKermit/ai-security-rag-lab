def generate_answer(query, top_result):
    name = top_result["name"]
    type_ = top_result.get("type", "unknown")
    description = top_result["description"]
    mitigation = top_result.get("mitigation", "No mitigation available.")
    aliases = ", ".join(top_result.get("aliases", []))

    answer = []

    answer.append(f"AI Security Insight for '{query}':")
    answer.append("")
    answer.append(f"{name} is the most relevant result for your query.")
    answer.append("")
    answer.append("Type:")
    answer.append(type_)
    answer.append("")
    answer.append("What it is:")
    answer.append(description)
    answer.append("")
    answer.append("Why it matters:")

    if type_ == "vulnerability":
        answer.append(
            "This vulnerability can be abused by attackers to bypass protections, access sensitive data, or compromise application behavior."
        )
    elif type_ == "attack":
        answer.append(
            "This attack pattern matters because it shows how attackers can exploit weaknesses in realistic offensive scenarios."
        )
    elif type_ == "technique":
        answer.append(
            "This technique matters because security testers and researchers use it to discover weaknesses in applications and systems."
        )
    elif type_ == "topic":
        answer.append(
            "This topic matters because it represents an important area of security knowledge that supports stronger testing, analysis, and defense."
        )
    else:
        answer.append(
            "This result is security-relevant and may help explain the user's query."
        )

    answer.append("")
    answer.append("Common aliases:")
    answer.append(aliases if aliases else "No aliases available.")
    answer.append("")
    answer.append("Basic mitigation / handling:")
    answer.append(mitigation)
    answer.append("")
    answer.append("Source:")
    answer.append("This answer is based on the internal structured security knowledge dataset.")

    return "\n".join(answer)
