import streamlit as st

from src.loader import load_vulnerabilities
from src.search import lexical_score, normalize_text
from src.semantic_search import semantic_scores, prepare_documents
from src.answer_generator import generate_answer


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

        # Exact / alias match override
        if query_lower == name_lower or query_lower in aliases:
            final_score = 100.0
        else:
            final_score = lex_score + sem_score

        results.append((final_score, vuln))

    results.sort(key=lambda x: x[0], reverse=True)
    return results[:3]


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

        top_score, top_vuln = results[0]

        STRONG_THRESHOLD = 4.0
        WEAK_THRESHOLD = 1.5

        if top_score < WEAK_THRESHOLD:
            st.warning("No strong match found. Try a more specific query.")
            st.stop()

        elif top_score < STRONG_THRESHOLD:
            st.info("Did you mean:")

            for score, vuln in results:
                st.write(f"- **{vuln['name']}** ({score:.4f})")

            st.stop()

        st.subheader("Best Match")
        st.markdown(f"```text\n{generate_answer(query, top_vuln)}\n```")

        st.metric("Confidence Score", f"{top_score:.4f}")

        if len(results) > 1:
            st.subheader("Other Matches")
            for score, vuln in results[1:]:
                st.write(f"- **{vuln['name']}** ({score:.4f})")
    else:
        st.warning("Please enter a valid query.")
