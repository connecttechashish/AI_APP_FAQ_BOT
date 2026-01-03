import json
from pathlib import Path

import faiss
import numpy as np


def _normalize(vectors):
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return vectors / norms


def build_index(chunks, model, index_dir="artifacts/index"):
    index_path = Path(index_dir)
    index_path.mkdir(parents=True, exist_ok=True)

    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    embeddings = embeddings.astype("float32")
    embeddings = _normalize(embeddings)

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, str(index_path / "index.faiss"))
    with (index_path / "metadata.json").open("w", encoding="utf-8") as handle:
        json.dump(chunks, handle, ensure_ascii=False, indent=2)

    return index


def load_index(index_dir="artifacts/index"):
    index_path = Path(index_dir)
    index_file = index_path / "index.faiss"
    meta_file = index_path / "metadata.json"

    if not index_file.exists() or not meta_file.exists():
        raise FileNotFoundError("Index not found. Run scripts/rebuild_index.ps1.")

    index = faiss.read_index(str(index_file))
    with meta_file.open("r", encoding="utf-8") as handle:
        metadata = json.load(handle)

    return index, metadata


def retrieve(query, k=3, model=None, index_dir="artifacts/index"):
    if model is None:
        from .embedding import load_embedding_model

        model = load_embedding_model()

    index, metadata = load_index(index_dir)

    query_vector = model.encode([query], convert_to_numpy=True, show_progress_bar=False)
    query_vector = query_vector.astype("float32")
    query_vector = _normalize(query_vector)

    scores, ids = index.search(query_vector, k)

    results = []
    for rank, idx in enumerate(ids[0].tolist()):
        if idx < 0 or idx >= len(metadata):
            continue
        item = dict(metadata[idx])
        item["score"] = float(scores[0][rank])
        results.append(item)

    return results
