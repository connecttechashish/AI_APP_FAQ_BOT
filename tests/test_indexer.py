from model.indexer import load_faq_chunks


def test_indexer_splits_by_heading():
    chunks = load_faq_chunks("data/faq.md")

    assert len(chunks) == 4

    questions = [chunk["question"] for chunk in chunks]
    assert questions == [
        "What is this project?",
        "Where does the FAQ content live?",
        "How do I add a new question?",
        "Does this require internet access?",
    ]

    for chunk in chunks:
        assert "Q: " in chunk["text"]
        assert "A: " in chunk["text"]
        assert chunk["answer"]
