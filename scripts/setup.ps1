# Create virtual environment and install dependencies
$venvPath = Join-Path $PSScriptRoot '..\.venv'

if (-not (Test-Path $venvPath)) {
  python -m venv $venvPath
}

& (Join-Path $venvPath 'Scripts\python.exe') -m pip install --upgrade pip
& (Join-Path $venvPath 'Scripts\pip.exe') install -r (Join-Path $PSScriptRoot '..\requirements.txt')
