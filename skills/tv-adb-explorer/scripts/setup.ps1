param([string]$ToolsDir = "$env:LOCALAPPDATA\TVAdbExplorer", [switch]$AcceptAndroidSdkLicense)
$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force -Path $ToolsDir | Out-Null
$adb = Get-Command adb.exe -ErrorAction SilentlyContinue
if ($adb) { $adbPath = $adb.Source } else { $adbPath = Join-Path $ToolsDir 'platform-tools\adb.exe' }
if (-not (Test-Path $adbPath)) {
    if (-not $AcceptAndroidSdkLicense) {
        throw 'Review Android SDK license at https://developer.android.com/tools/releases/platform-tools then rerun with -AcceptAndroidSdkLicense if accepted. Or supply your existing official platform-tools.'
    }
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    $zip = Join-Path $ToolsDir 'platform-tools.zip'
    Invoke-WebRequest 'https://dl.google.com/android/repository/platform-tools-latest-windows.zip' -OutFile $zip -UseBasicParsing
    Expand-Archive -Path $zip -DestinationPath $ToolsDir -Force
    Remove-Item $zip
}
& $adbPath version
if ($LASTEXITCODE -ne 0) { throw 'ADB could not run.' }
& $adbPath devices -l
if ($LASTEXITCODE -ne 0) { throw 'ADB devices failed.' }
$config = @{ adb = $adbPath; configured_at = (Get-Date).ToString('o') }
$config | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $ToolsDir 'config.json')
Write-Host "ADB configuration saved to $ToolsDir\config.json"
Write-Host 'USB prerequisite: TV must expose a USB device/debug port. A normal TV host USB port is not sufficient.'
Write-Host 'No device: check OEM debug port/cable and OEM Windows ADB driver. unauthorized: accept RSA prompt on TV.'
Write-Host 'Before overnight run: install Python 3.10+ and official Codex CLI, then complete codex login interactively.'
