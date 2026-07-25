# Run the offline pipeline (pass-through args). E.g.:  ./scripts/precompute.ps1 EX02_epidemic --seed 7
$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path (Join-Path $PSScriptRoot ".."))
$candidates = @(
  (Join-Path (Get-Location) ".venv-pipeline\Scripts\python.exe"),
  (Join-Path (Get-Location) ".venv-pipeline\bin\python"),
  (Join-Path (Get-Location) ".venv\Scripts\python.exe"),
  (Join-Path (Get-Location) ".venv\bin\python")
)
$vp = $candidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $vp) {
  throw "No repository Python environment found. Run scripts/setup.ps1 first."
}
$pipelinePath = Join-Path (Get-Location) "data-pipeline"
$env:PYTHONPATH = if ($env:PYTHONPATH) {
  "$pipelinePath$([IO.Path]::PathSeparator)$env:PYTHONPATH"
} else {
  $pipelinePath
}
& $vp -m researchlab.pipeline @args
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}
