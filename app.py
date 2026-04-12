import streamlit as st

from src.loader import load_vulnerabilities
from src.search import lexical_score, normalize_text
from src.semantic_search import semantic_scores, prepare_documents
from src.answer_generator import generate_answer
from src.context_builder import build_context
from src.llm_client import generate_llm_answer


# -----------------------------
# Data loading
# -----------------------------
file_path = "data/vulns.json"
vulnerabilities = load_vulnerabilities(file_path)
_, doc_embeddings = prepare_documents(vulnerabilities)


# -----------------------------
# Search logic
# -----------------------------
def search(query: str):
    semantic = semantic_scores(query, doc_embeddings)
    query_lower = query.lower()

    results = []
    for i, vuln in enumerate(vulnerabilities):
        lex_score = lexical_score(query, vuln)
        sem_score = semantic[i]

        aliases = [alias.lower() for alias in vuln.get("aliases", [])]
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


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(
    page_title="AI Security RAG Lab",
    page_icon="🛡️",
    layout="wide",
)

st.title("AI Security RAG Lab")
st.caption(
    "Type-aware security knowledge retrieval for vulnerabilities, attacks, techniques, and topics."
)

st.write(
    "Search for vulnerabilities, attack patterns, security techniques, or security topics."
)

query = st.text_input("Enter your query:")

if query:
    normalized_query = normalize_text(query)

    if normalized_query:
        results = search(normalized_query)

        top_result = results[0]
        top_score = top_result["final_score"]
        top_vuln = top_result["vuln"]

        if top_score < WEAK_THRESHOLD:
            st.warning("No strong match found. Try a more specific query.")
            st.caption(build_confidence_explanation(top_result))
            st.stop()

        elif top_score < STRONG_THRESHOLD:
            st.info("Did you mean:")
            st.caption(build_confidence_explanation(top_result))

            for result in results:
                vuln = result["vuln"]
                score = result["final_score"]
                st.write(f"- **{vuln['name']}** ({score:.4f})")

            st.stop()

        fallback_answer = generate_answer(query, top_vuln)
        context = build_context(query, top_result, results[1:])
        final_answer = generate_llm_answer(context, fallback_answer)

        st.subheader("Best Match")
        st.caption("Source: Internal AI Security Knowledge Base")
        st.markdown(f"```text\n{final_answer}\n```")

        st.metric("Confidence Score", f"{top_score:.4f}")
        st.caption(build_confidence_explanation(top_result))

        if len(results) > 1:
            st.subheader("Other Matches")
            for result in results[1:]:
                vuln = result["vuln"]
                score = result["final_score"]
                st.write(f"- **{vuln['name']}** ({score:.4f})")
    else:
        st.warning("Please enter a valid query.")
