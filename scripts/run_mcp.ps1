# Start the local JSON tool server
$venvPath = Join-Path $PSScriptRoot '..\.venv'

& (Join-Path $venvPath 'Scripts\python.exe') -m mcp_server.server
