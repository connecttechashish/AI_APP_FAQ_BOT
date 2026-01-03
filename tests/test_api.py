from fastapi.testclient import TestClient

from app.main import app, agent


def test_health():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_chat_returns_answer_with_citations(monkeypatch):
    def fake_chat(_query):
        return "Here is the answer.\n\nSources:\n[1] Example"

    monkeypatch.setattr(agent, "chat", fake_chat)

    client = TestClient(app)
    response = client.post("/chat", json={"query": "Where does the FAQ content live?"})
    assert response.status_code == 200
    payload = response.json()
    assert "response" in payload
    assert "Sources:" in payload["response"]
