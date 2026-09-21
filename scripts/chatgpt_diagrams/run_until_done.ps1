# Keep PC awake and resume Mastering MongoDB ChatGPT diagrams until the queue is empty.
# Same overnight pattern as MD287 new-PPT diagram generation.
$ErrorActionPreference = "Continue"

$ToolDir = $PSScriptRoot
$Repo = (Resolve-Path (Join-Path $ToolDir "..\..")).Path
$GenAll = Join-Path $ToolDir "generate_all.py"
$LogFile = Join-Path $ToolDir "runner.log"

Set-Location $Repo
$env:PYTHONUNBUFFERED = "1"
$env:PYTHONIOENCODING = "utf-8"

Add-Type -Namespace Native -Name Power -MemberDefinition @"
[DllImport("kernel32.dll")]
public static extern uint SetThreadExecutionState(uint esFlags);
"@ -ErrorAction SilentlyContinue
function Prevent-Sleep {
  [void][Native.Power]::SetThreadExecutionState([uint32]"0x80000003")
}
function Allow-Sleep {
  [void][Native.Power]::SetThreadExecutionState([uint32]"0x80000000")
}

function Write-Log([string]$Message) {
  $line = "[{0}] {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Message
  Write-Host $line
  Add-Content -Path $LogFile -Value $line -Encoding UTF8
}

function Get-QueuedCount {
  $out = & python $GenAll --dry-run 2>&1 | Out-String
  $total = 0
  $matches = [regex]::Matches($out, "queued:\s*(\d+)")
  foreach ($m in $matches) { $total += [int]$m.Groups[1].Value }
  if ($matches.Count -eq 0) {
    Write-Log ("WARN: dry-run parse failed. Tail: " + ($out.Substring([Math]::Max(0, $out.Length - 600))))
    return -1
  }
  return $total
}

try {
  Prevent-Sleep
  Write-Log "Keep-awake ON. Mastering MongoDB HD diagrams (ChatGPT/Playwright) until queue empty."
  Write-Log "Repo: $Repo"

  $round = 0
  $quotaHits = 0
  while ($true) {
    $round++
    Prevent-Sleep
    $queued = Get-QueuedCount
    Write-Log ("======== Round {0} | queued={1} ========" -f $round, $queued)

    if ($queued -eq 0) {
      Write-Log "ALL_MONGODB_DIAGRAMS_DONE"
      break
    }

    Write-Log ">> python generate_all.py"
    & python $GenAll --new-chat-every 8 --pause-ms 2000 --timeout 240 --login-timeout 900
    $code = $LASTEXITCODE
    Write-Log ("Generation exit code: {0}" -f $code)

    $quotaPause = 45
    $joined = ""
    Get-ChildItem -LiteralPath $ToolDir -Filter "diagrams_module*_results.csv" -ErrorAction SilentlyContinue |
      ForEach-Object { $joined += ((Get-Content $_.FullName -Tail 8 -ErrorAction SilentlyContinue) -join "`n") + "`n" }
    $logDir = Join-Path $ToolDir "diagrams_logs"
    if (Test-Path $logDir) {
      $latestTxt = Get-ChildItem -LiteralPath $logDir -Recurse -Filter "timeout_*.txt" -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending | Select-Object -First 1
      if ($latestTxt -and $latestTxt.LastWriteTime -gt (Get-Date).AddMinutes(-30)) {
        $joined += Get-Content -LiteralPath $latestTxt.FullName -Raw -ErrorAction SilentlyContinue
      }
    }
    if ($code -eq 3 -or $joined -match "Plus plan limit|limit resets in|QUOTA:|image generation limit|quota exhausted|image generations requests") {
      $quotaHits++
      if ($joined -match "limit resets in\s+(\d+)\s+hours?(?:\s+and\s+(\d+)\s+minutes?)?") {
        $hours = [int]$Matches[1]
        $mins = if ($Matches[2]) { [int]$Matches[2] } else { 0 }
        $quotaPause = [Math]::Max(3600, (($hours * 3600) + ($mins * 60) + 600))
      } else {
        $quotaPause = [Math]::Min(7200, 1800 * [Math]::Max(1, $quotaHits))
      }
      Write-Log ("QUOTA detected (hit #{0}). Sleeping {1}s (~{2:N1}h) before resume." -f $quotaHits, $quotaPause, ($quotaPause / 3600.0))
    } elseif ($joined -match "logged in|login|Timed out waiting for ChatGPT login") {
      $quotaPause = 120
      Write-Log "Login/session issue — waiting 120s before retry."
    } else {
      $quotaHits = 0
    }

    Prevent-Sleep
    Write-Log ("Pausing {0}s before resume check..." -f $quotaPause)
    $remaining = $quotaPause
    while ($remaining -gt 0) {
      Prevent-Sleep
      $chunk = [Math]::Min(240, $remaining)
      Start-Sleep -Seconds $chunk
      $remaining -= $chunk
    }
  }
}
finally {
  Allow-Sleep
  Write-Log "Keep-awake OFF."
}
