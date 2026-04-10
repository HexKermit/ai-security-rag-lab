from sentence_transformers import SentenceTransformer, util


model = SentenceTransformer("all-MiniLM-L6-v2")


def build_search_text(vuln):
    return f"{vuln['name']} {' '.join(vuln['aliases'])} {vuln['description']}"


def semantic_search(query, vulnerabilities, top_k=3):
    documents = [build_search_text(vuln) for vuln in vulnerabilities]

    doc_embeddings = model.encode(documents, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)

    scores = util.cos_sim(query_embedding, doc_embeddings)[0]

    scored_results = []
    for i, score in enumerate(scores):
        scored_results.append((float(score), vulnerabilities[i]))

    scored_results.sort(reverse=True, key=lambda x: x[0])
    return scored_results[:top_k]
