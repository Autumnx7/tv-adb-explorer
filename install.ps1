param([string]$Destination = (Join-Path $env:USERPROFILE '.agents\skills\tv-adb-explorer'))
$ErrorActionPreference = 'Stop'
$source = Join-Path $PSScriptRoot 'skills\tv-adb-explorer'
if (-not (Test-Path (Join-Path $source 'SKILL.md'))) { throw 'Run from the extracted repository folder.' }
if (Test-Path $Destination) { throw "Already exists: $Destination. Review changes and back up the old skill before replacing it." }
New-Item -ItemType Directory -Force -Path (Split-Path $Destination) | Out-Null
Copy-Item -Path $source -Destination $Destination -Recurse
Write-Host "Installed: $Destination"
Write-Host 'Open a new Codex chat and ask to use $tv-adb-explorer. Runtime dependencies are checked separately.'
