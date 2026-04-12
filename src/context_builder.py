def build_context(query, top_result, related_results):
    top_vuln = top_result["vuln"]

    context = []
    context.append(f"User query: {query}")
    context.append("")
    context.append("Primary match:")
    context.append(f"- Name: {top_vuln['name']}")
    context.append(f"- Type: {top_vuln.get('type', 'unknown')}")
    context.append(f"- Description: {top_vuln['description']}")
    context.append(f"- Mitigation: {top_vuln.get('mitigation', 'N/A')}")
    context.append(f"- Confidence Score: {top_result['final_score']:.4f}")
    context.append("")

    if related_results:
        context.append("Related matches:")
        for result in related_results:
            vuln = result["vuln"]
            context.append(
                f"- {vuln['name']} | type={vuln.get('type', 'unknown')} | score={result['final_score']:.4f}"
            )
        context.append("")

    context.append("Instruction:")
    context.append(
        "Use only the provided context. Do not invent facts. "
        "Explain the result clearly and practically."
    )

    return "\n".join(context)
