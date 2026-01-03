import numpy as np

from model.indexer import load_faq_chunks
from model.vectorstore import build_index, retrieve


class DummyEmbeddingModel:
    def __init__(self, keywords):
        self.keywords = keywords

    def encode(self, texts, convert_to_numpy=True, show_progress_bar=False):
        vectors = []
        for text in texts:
            text_lower = text.lower()
            vec = [text_lower.count(keyword) for keyword in self.keywords]
            vectors.append(vec)
        array = np.asarray(vectors, dtype="float32")
        return array if convert_to_numpy else array.tolist()


def test_retrieve_returns_expected_section(tmp_path):
    keywords = ["project", "content", "internet"]
    model = DummyEmbeddingModel(keywords)
    chunks = load_faq_chunks("data/faq.md")

    build_index(chunks, model, index_dir=tmp_path)

    results = retrieve(
        "where is the faq content stored?",
        k=1,
        model=model,
        index_dir=tmp_path,
    )

    assert results
    assert results[0]["question"] == "Where does the FAQ content live?"
