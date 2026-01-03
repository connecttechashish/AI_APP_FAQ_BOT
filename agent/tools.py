from model.vectorstore import retrieve


def retrieve_faq(query, k=3, threshold=0.3, index_dir="artifacts/index"):
    results = retrieve(query, k=k, index_dir=index_dir)
    top_score = results[0]["score"] if results else 0.0
    low_confidence = top_score < threshold
    return results, low_confidence
