from sentence_transformers import SentenceTransformer, util

MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)


def build_search_text(vuln):
    return f"{vuln['name']} {' '.join(vuln['aliases'])} {vuln['description']}"


def semantic_scores(query, vulnerabilities):
    documents = [build_search_text(vuln) for vuln in vulnerabilities]

    doc_embeddings = model.encode(documents, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)

    scores = util.cos_sim(query_embedding, doc_embeddings)[0]

    return [float(score) for score in scores]
