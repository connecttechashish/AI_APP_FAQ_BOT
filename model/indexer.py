from pathlib import Path
import re


def split_faq_by_heading(text):
    pattern = re.compile(r"^##\s+(.*)", re.M)
    matches = list(pattern.finditer(text))
    chunks = []

    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        question = match.group(1).strip()
        answer = text[start:end].strip()
        if not answer:
            continue
        chunk_text = f"Q: {question}\nA: {answer}"
        chunks.append(
            {
                "id": len(chunks),
                "question": question,
                "answer": answer,
                "text": chunk_text,
            }
        )

    return chunks


def load_faq_chunks(path="data/faq.md"):
    text = Path(path).read_text(encoding="utf-8")
    return split_faq_by_heading(text)
