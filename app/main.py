import os
from pathlib import Path

from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse

from agent import FAQAgent
from model.embedding import load_embedding_model
from model.indexer import load_faq_chunks
from model.vectorstore import build_index

app = FastAPI(title="FAQ Bot")


def _bool_env(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


agent = FAQAgent(use_ollama=_bool_env("FAQ_USE_OLLAMA"))


def _ensure_index(index_dir="artifacts/index", faq_path="data/faq.md"):
    index_path = Path(index_dir)
    if (index_path / "index.faiss").exists() and (index_path / "metadata.json").exists():
        return
    chunks = load_faq_chunks(faq_path)
    model = load_embedding_model()
    build_index(chunks, model, index_dir=index_dir)


@app.on_event("startup")
def startup():
    try:
        _ensure_index()
    except Exception:
        pass


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/chat")
def chat(payload: dict):
    query = (payload or {}).get("query", "").strip()
    if not query:
        raise HTTPException(status_code=400, detail="query is required")
    try:
        _ensure_index()
        response = agent.chat(query)
        return {"response": response}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/reindex")
def reindex():
    try:
        chunks = load_faq_chunks("data/faq.md")
        model = load_embedding_model()
        build_index(chunks, model)
        return {"ok": True, "count": len(chunks)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/", response_class=HTMLResponse)
def ui():
    return _render_ui()


@app.post("/ui", response_class=HTMLResponse)
def ui_post(query: str = Form("")):
    answer = ""
    if query.strip():
        try:
            _ensure_index()
            answer = agent.chat(query.strip())
        except Exception as exc:
            answer = f"Error: {exc}"
    return _render_ui(query=query, answer=answer)


def _render_ui(query="", answer=""):
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>FAQ Bot</title>
    <style>
      body {{ font-family: "Segoe UI", Tahoma, sans-serif; margin: 32px; }}
      .container {{ max-width: 720px; margin: 0 auto; }}
      textarea {{ width: 100%; min-height: 110px; padding: 12px; }}
      button {{ padding: 8px 16px; margin-top: 12px; }}
      pre {{ background: #f6f6f6; padding: 12px; white-space: pre-wrap; }}
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Local FAQ Bot</h1>
      <form method="post" action="/ui">
        <label for="query">Question</label>
        <textarea id="query" name="query">{query}</textarea>
        <br />
        <button type="submit">Ask</button>
      </form>
      <h2>Answer</h2>
      <pre>{answer}</pre>
    </div>
  </body>
</html>"""
