# Start FastAPI using uvicorn
$venvPath = Join-Path $PSScriptRoot '..\.venv'

& (Join-Path $venvPath 'Scripts\uvicorn.exe') app.main:app --reload --host 127.0.0.1 --port 8000
