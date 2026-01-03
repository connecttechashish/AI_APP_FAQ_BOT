from pathlib import Path

from model.embedding import load_embedding_model
from model.indexer import load_faq_chunks
from model.vectorstore import build_index, retrieve


def _ensure_index(index_dir="artifacts/index", faq_path="data/faq.md"):
    index_path = Path(index_dir)
    if (index_path / "index.faiss").exists() and (index_path / "metadata.json").exists():
        return
    chunks = load_faq_chunks(faq_path)
    model = load_embedding_model()
    build_index(chunks, model, index_dir=index_dir)


def retrieve_faq(query, k=3, threshold=0.3, index_dir="artifacts/index"):
    _ensure_index(index_dir=index_dir)
    results = retrieve(query, k=k, index_dir=index_dir)
    top_score = results[0]["score"] if results else 0.0
    low_confidence = top_score < threshold
    return {"results": results, "low_confidence": low_confidence}


def list_docs(path="data/faq.md"):
    chunks = load_faq_chunks(path)
    return [{"id": chunk["id"], "question": chunk["question"]} for chunk in chunks]


def reload_index(path="data/faq.md", index_dir="artifacts/index"):
    chunks = load_faq_chunks(path)
    model = load_embedding_model()
    build_index(chunks, model, index_dir=index_dir)
    return {"ok": True, "count": len(chunks)}
