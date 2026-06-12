# Start Django development server on port 8080.
# Prefer a local virtual environment if one exists, otherwise use python from PATH.

$ErrorActionPreference = 'Stop'

Set-Location $PSScriptRoot

$python = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $python)) {
	$python = (Get-Command python -ErrorAction Stop).Source
}

& $python manage.py runserver 8080
