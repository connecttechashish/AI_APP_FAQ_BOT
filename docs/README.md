# Docs

## Quickstart

1. `scripts/setup.ps1`
2. `scripts/run.ps1`
3. Open `http://127.0.0.1:8000/`

The app will auto-build the FAQ index if it is missing. You can also rebuild it manually with `scripts/rebuild_index.ps1` or `POST /reindex`.

## API

- `GET /health`
- `POST /chat` with JSON `{"query":"..."}`
- `POST /reindex`

## Local tool server

Run `scripts/run_mcp.ps1` to start a minimal JSON tool server on `http://127.0.0.1:8765`.

Example request:

```json
{"tool":"retrieve_faq","args":{"query":"Where does the FAQ content live?","k":1}}
```

## Windows setup note

If you see a Torch DLL error like WinError 126, install the Microsoft Visual C++ Redistributable (VS 2015-2022, x64). The `requirements.txt` includes the CPU-only PyTorch index so installs pull CPU wheels by default.

## Troubleshooting

- If `faiss` import fails, make sure you're using the project venv.
- Ensure the active Python interpreter is 64-bit and points at `.venv`.
