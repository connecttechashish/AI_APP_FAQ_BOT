# Runbook

## Start the API

1. `scripts/setup.ps1`
2. `scripts/run.ps1`

The UI is available at `http://127.0.0.1:8000/`.

## Rebuild the index

Use either:
- `scripts/rebuild_index.ps1` (offline rebuild)
- `POST /reindex` on the API

## Tool server

Start the local tool server:
- `scripts/run_mcp.ps1`

## Troubleshooting

- If you see WinError 126 for Torch DLLs, install the VC++ 2015-2022 x64 runtime.
- If `faiss` import fails, make sure you're using the project venv.
