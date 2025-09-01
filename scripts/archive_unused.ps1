<#
Safe archiving script for suspected unused project files.
Place this script in the repository and run from PowerShell.
By default it will move known large/untracked candidates into a timestamped archive directory.
Run with -IncludeVenv to also move the local virtual environment (be careful; large).
#>
param(
    [switch]$IncludeVenv
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
# assume script lives in <repo>/scripts, so repo root is parent of script dir
$root = Split-Path -Parent $scriptDir
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$archive = Join-Path $root "archive_unused_$timestamp"

Write-Host "Creating archive folder: $archive"
New-Item -ItemType Directory -Path $archive -Force | Out-Null

$items = @(
    "Cycleoflife.html",
    "Self Mastery and Fate With the Cycles of Life - H. Spencer Lewis.pdf",
    "package-lock.json",
    "package.json",
    "package-lock.json",
    "package-lock.yaml",
    "venv",
    ".venv",
    "node_modules"
)

$log = Join-Path $archive "archive_log.txt"
Add-Content -Path $log -Value "Archive run at: $(Get-Date -Format o)"
Add-Content -Path $log -Value "Root: $root"

foreach ($name in $items) {
    # Skip venv unless requested
    if (($name -eq 'venv' -or $name -eq '.venv' -or $name -ieq 'node_modules') -and -not $IncludeVenv) {
        Write-Host "Skipping $name (use -IncludeVenv to include venv/node_modules)"
        Add-Content -Path $log -Value "Skipped: $name"
        continue
    }

    $path = Join-Path $root $name
    if (Test-Path $path) {
        try {
            Write-Host "Moving $path -> $archive"
            Move-Item -Path $path -Destination $archive -Force
            Add-Content -Path $log -Value "Moved: $path"
        } catch {
            $err = $_.Exception.Message
            Write-Host ("Failed to move {0}: {1}" -f $path, $err) -ForegroundColor Yellow
            Add-Content -Path $log -Value ("Failed: {0} -> {1}" -f $path, $err)
        }
    } else {
        Add-Content -Path $log -Value "Not found: $path"
    }
}

Write-Host "Archive complete. See $log for details." -ForegroundColor Green

# Suggest next steps
Write-Host "To review archived files: explorer.exe `"$archive`"" -ForegroundColor Cyan
Write-Host "To restore a file, move it back from the archive folder to the repo root." -ForegroundColor Cyan
