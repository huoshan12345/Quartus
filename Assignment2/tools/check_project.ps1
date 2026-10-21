$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$quartusMap = 'C:\intelFPGA_lite\20.1\quartus\bin64\quartus_map.exe'
Push-Location -LiteralPath $projectRoot
try {
    New-Item -ItemType Directory -Force -Path 'verification' | Out-Null
    foreach ($revision in @('counter16', 'counter12', 'register8', 'register16', 'bus16_mux8')) {
        & $quartusMap assignment2 -c $revision --analysis_and_elaboration |
            Tee-Object -FilePath (Join-Path 'verification' ($revision + '_elaboration.log'))
        if ($LASTEXITCODE -ne 0) {
            throw "Quartus check failed for $revision"
        }
    }
} finally {
    Pop-Location
}
