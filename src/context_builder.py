def build_context(query, top_vuln, related_vulns):
    context = []

    context.append(f"User query: {query}\n")

    context.append("Primary match:")
    context.append(f"- Name: {top_vuln['name']}")
    context.append(f"- Type: {top_vuln.get('type', 'unknown')}")
    context.append(f"- Description: {top_vuln['description']}")
    context.append(f"- Mitigation: {top_vuln.get('mitigation', 'N/A')}\n")

    if related_vulns:
        context.append("Related concepts:")
        for vuln in related_vulns:
            context.append(f"- {vuln['name']} ({vuln.get('type', 'unknown')})")

    return "\n".join(context)
