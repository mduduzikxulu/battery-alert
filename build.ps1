$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

python -m pip install -r requirements-build.txt
if ($LASTEXITCODE -ne 0) {
    throw "Failed to install build requirements."
}

python create_icon.py
if ($LASTEXITCODE -ne 0) {
    throw "Failed to create the application icon."
}

python -m PyInstaller --noconfirm --clean --onefile --windowed `
    --name BatteryAlert --icon battery_alert.ico `
    --collect-submodules pystray app.py
if ($LASTEXITCODE -ne 0) {
    throw "Failed to package Battery Alert."
}

$compiler = Join-Path ${env:ProgramFiles(x86)} "Inno Setup 6\ISCC.exe"
if (-not (Test-Path -LiteralPath $compiler)) {
    $compiler = Join-Path $env:ProgramFiles "Inno Setup 6\ISCC.exe"
}
if (-not (Test-Path -LiteralPath $compiler)) {
    $compiler = Join-Path $env:LOCALAPPDATA "Programs\Inno Setup 6\ISCC.exe"
}
if (-not (Test-Path -LiteralPath $compiler)) {
    throw "Inno Setup 6 was not found. Install it from https://jrsoftware.org/isinfo.php, then run this script again."
}

New-Item -ItemType Directory -Force -Path (Join-Path $root "dist\installer") | Out-Null
& $compiler (Join-Path $root "BatteryAlert.iss")
if ($LASTEXITCODE -ne 0) {
    throw "Failed to build the Windows installer."
}

Write-Host "Installer created at $root\dist\installer\BatteryAlert-Setup.exe"
