# Avvio locale Windows PowerShell: aggiorna il database SQLite locale.

$ProjectDir = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectDir

$env:PYTHONPATH = "src"
$Python = Join-Path $ProjectDir ".venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    $Python = "python"
}

& $Python -m albo_monitor.main fetch --max-pages 5
