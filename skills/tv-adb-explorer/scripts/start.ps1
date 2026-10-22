param(
    [Parameter(Mandatory=$true)][string]$Package,
    [Parameter(Mandatory=$true)][string]$Serial,
    [Parameter(Mandatory=$true)][string]$Out,
    [string]$Adb,
    [string]$Activity,
    [double]$Hours = 8,
    [int]$MaxSteps = 1200,
    [switch]$Background
)
$ErrorActionPreference = 'Stop'
if (-not $Adb) {
    $config = Get-Content -Raw "$env:LOCALAPPDATA\TVAdbExplorer\config.json" | ConvertFrom-Json
    $Adb = $config.adb
}
if (-not (Test-Path $Adb)) { throw 'ADB missing. Run setup.ps1 first.' }
$python = Get-Command python.exe -ErrorAction SilentlyContinue
$prefix = @()
$launcher = Get-Command py.exe -ErrorAction SilentlyContinue
if ($launcher) { $python = $launcher; $prefix = @('-3') }
if (-not $python) { throw 'Install Python 3.10+ from python.org or official Windows package, then retry.' }
& $python.Source @prefix -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)'
if ($LASTEXITCODE -ne 0) { throw 'A working Python 3.10+ is required.' }
if (-not (Get-Command codex -ErrorAction SilentlyContinue)) { throw 'Official Codex CLI not found on PATH. Install it and complete codex login first.' }
New-Item -ItemType Directory -Force -Path $Out | Out-Null
$Out = (Resolve-Path $Out).Path
if (Test-Path (Join-Path $Out 'STOP')) { throw 'STOP file exists. Remove it only when you intend to resume.' }
$argsList = $prefix + @((Join-Path $PSScriptRoot 'explore.py'), '--adb', $Adb, '--serial', $Serial, '--package', $Package, '--out', $Out, '--hours', $Hours.ToString([cultureinfo]::InvariantCulture), '--max-steps', "$MaxSteps")
if ($Activity) { $argsList += @('--activity', $Activity) }
if ($Background) {
    # Windows file paths cannot contain double quotes. Reject them in free text too.
    foreach ($value in $argsList) { if ($value.Contains('"')) { throw 'Double quotes are not supported in arguments.' } }
    $quoted = ($argsList | ForEach-Object { '"' + $_ + '"' }) -join ' '
    $process = Start-Process -FilePath $python.Source -ArgumentList $quoted -WorkingDirectory $Out -RedirectStandardOutput (Join-Path $Out 'runner.stdout.log') -RedirectStandardError (Join-Path $Out 'runner.stderr.log') -PassThru
    Write-Host "Started PID $($process.Id). Inspect state.json and runner.stderr.log before leaving it unattended."
} else {
    & $python.Source @argsList
    if ($LASTEXITCODE -ne 0) { throw "Explorer exited with code $LASTEXITCODE; see events.jsonl." }
}
