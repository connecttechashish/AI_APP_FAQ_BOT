
---

# 🧠 Local AI FAQ Bot (End-to-End RAG System)

> **An end-to-end AI FAQ Bot built locally on Windows using Python, FastAPI, and Retrieval-Augmented Generation (RAG).**
> Designed, developed, tested, and deployed **from scratch** to demonstrate real-world AI system architecture.

---

## 🚀 Project Overview

This project demonstrates how to build a **production-style AI application** locally without relying on paid cloud services.

The system:

* Ingests FAQ documents
* Builds embeddings and a vector index
* Uses an **agent-based RAG pipeline**
* Exposes tools via an **MCP-style server**
* Serves a **FastAPI backend + simple chat UI**
* Includes **tests, scripts, and documentation**

Everything runs on a **local Windows machine using VS Code**.

---

## 🎯 Key Features

* ✅ Local **Retrieval-Augmented Generation (RAG)**
* ✅ Modular **Model / Agent / App** architecture
* ✅ Tool-calling **AI Agent**
* ✅ MCP-style tool server
* ✅ FastAPI REST API
* ✅ Simple Chat UI
* ✅ Full test coverage (unit + API)
* ✅ Windows PowerShell scripts for automation
* ✅ Beginner-friendly, readable code

---

## 🧩 Architecture

```
User
 ↓
Web UI / API (FastAPI)
 ↓
AI Agent (tool-using RAG)
 ↓
Retrieval Tools
 ↓
Vector Store (FAISS)
 ↓
Embeddings (Sentence Transformers)
 ↓
FAQ Documents (Markdown)
```

### Why this design?

* **Separation of concerns** (model ≠ agent ≠ app)
* Easy to extend (swap UI, models, tools)
* Mirrors real production AI systems

---

## 📁 Repository Structure

```
.
├── data/                 # FAQ knowledge base
│   └── faq.md
├── model/                # Embeddings, chunking, vector index
│   ├── indexer.py
│   ├── embedding.py
│   └── vectorstore.py
├── agent/                # RAG agent & tools
│   ├── agent.py
│   ├── tools.py
│   └── prompts.py
├── mcp_server/           # MCP-style tool server
│   ├── server.py
│   └── tools.py
├── app/                  # FastAPI app & UI
│   ├── api.py
│   ├── config.py
│   └── ui.py
├── tests/                # Unit & integration tests
├── scripts/              # PowerShell automation
├── artifacts/            # Generated vector index (gitignored)
├── docs/                 # Architecture & runbooks
└── README.md
```

---

## 🛠️ Tech Stack

| Layer      | Technology                    |
| ---------- | ----------------------------- |
| Language   | Python 3.11+                  |
| API        | FastAPI                       |
| UI         | FastAPI Templates / Streamlit |
| Embeddings | sentence-transformers         |
| Vector DB  | FAISS (local)                 |
| Agent      | Custom tool-using RAG agent   |
| Testing    | pytest                        |
| Runtime    | Local Windows (PowerShell)    |

---

## ⚙️ Setup & Run (Local)

### 1️⃣ Clone Repo

```powershell
git clone <repo-url>
cd local-ai-faq-bot
```

### 2️⃣ Setup Environment

```powershell
.\scripts\setup.ps1
```

### 3️⃣ Build Vector Index

```powershell
.\scripts\rebuild_index.ps1
```

### 4️⃣ Run the App

```powershell
.\scripts\run.ps1
```

Open browser:

```
http://127.0.0.1:8000
```

---

## 🧪 Run Tests

```powershell
.\scripts\test.ps1
```

Expected:

```
All tests passed ✔
```

---

## 💬 Example Queries

| User Question                 | Bot Behavior                      |
| ----------------------------- | --------------------------------- |
| “How do I reset my password?” | Returns answer + citations        |
| “What plans do you offer?”    | Retrieves correct FAQ section     |
| “Do you support refunds?”     | Answers or asks for clarification |
| Unknown topic                 | Responds with “I don’t know”      |

---

## 🤖 Agent Behavior

The agent:

1. Retrieves top-k FAQ chunks
2. Scores relevance
3. If confident → answers with citations
4. If not confident → asks clarifying question
5. Never hallucinates beyond source data

Optional:

* Uses **Ollama** locally if available for better summarization
* Falls back to extractive answers if no LLM is installed

---

## 🔌 MCP Server

A minimal **MCP-style tool server** exposes:

* `retrieve_faq(query, k)`
* `list_docs()`
* `reload_index()`

This allows:

* Tool reuse
* Future multi-agent setups
* External agent integration

---

## 📚 Documentation

* `docs/ARCHITECTURE.md` — system design
* `docs/RUNBOOK.md` — debugging & local dev
* Inline code comments for learning

---

## 🎓 What This Project Demonstrates

✅ End-to-end AI system thinking
✅ Practical RAG implementation
✅ Agent & tool orchestration
✅ API + UI integration
✅ Testing AI systems
✅ Production-style repo hygiene

---

## 🔮 Possible Extensions

* Replace FAISS with Chroma
* Add persistent memory
* Add authentication
* Dockerize for deployment
* Multi-document ingestion
* Multi-agent workflows

---

## 👤 Author

** Software Engineer/AI Developer**
Built as a learning-focused portfolio project to demonstrate real-world AI application development.

---