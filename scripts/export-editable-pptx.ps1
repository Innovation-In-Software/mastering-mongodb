param(
    [Parameter(Mandatory = $true)]
    [string]$InputMd,

    [string]$OutputPptx = ""
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$inputPath = Join-Path $repoRoot $InputMd

if (-not (Test-Path $inputPath)) {
    throw "Markdown file not found: $inputPath"
}

if (-not $OutputPptx) {
    $base = [System.IO.Path]::GetFileNameWithoutExtension($inputPath)
    $OutputPptx = Join-Path (Split-Path $inputPath -Parent) "$base-editable-clean.pptx"
}

$rawPptx = Join-Path (Split-Path $OutputPptx -Parent) (([System.IO.Path]::GetFileNameWithoutExtension($OutputPptx)) + ".raw.pptx")
$theme = Join-Path $repoRoot "scripts/themes/flat-gaia.css"

if (-not (Test-Path $env:SOFFICE_PATH)) {
    $defaultSoffice = "C:\Program Files\LibreOffice\program\soffice.exe"
    if (Test-Path $defaultSoffice) {
        $env:SOFFICE_PATH = $defaultSoffice
    }
}

Write-Host "Exporting editable PPTX (flat-gaia theme)..."
Push-Location $repoRoot
npx @marp-team/marp-cli $inputPath `
    --theme $theme `
    --pptx --pptx-editable `
    --allow-local-files --no-stdin `
    -o $rawPptx

Write-Host "Cleaning decorative shapes..."
python (Join-Path $PSScriptRoot "clean-editable-pptx.py") $rawPptx `
    -o $OutputPptx `
    --mode text-only `
    --source-md $inputPath

Remove-Item $rawPptx -ErrorAction SilentlyContinue
Pop-Location

Write-Host "Done: $OutputPptx"
