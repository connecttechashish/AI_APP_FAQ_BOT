# Run tests with pytest
$venvPath = Join-Path $PSScriptRoot '..\.venv'

& (Join-Path $venvPath 'Scripts\pytest.exe')
