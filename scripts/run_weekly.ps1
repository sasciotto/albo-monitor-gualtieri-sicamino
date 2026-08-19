# Avvio locale Windows PowerShell.
# Prima crea .env partendo da .env.example.

$ProjectDir = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectDir

$env:PYTHONPATH = "src"
$Python = Join-Path $ProjectDir ".venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    $Python = "python"
}

& $Python -m albo_monitor.main telegram-weekly
