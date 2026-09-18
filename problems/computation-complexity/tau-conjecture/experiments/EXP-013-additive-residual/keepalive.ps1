# Self-healing launcher for the EXP-013 additive shards.
#
# Guard is COMMAND-LINE SPECIFIC on purpose: this machine runs other sessions'
# python work, so "is any python.exe running" is the wrong question (and acting
# on it once cost another session its processes).
#
# 2026-08-25 rewrite, after two defects that between them would have stalled the
# run permanently:
#   1. The old guard was "if ANY of my shards is running, do nothing". Combined
#      with $want = 10 and $N = 20 it always relaunched the FIRST ten needy
#      shards, so partitions in classes 10..19 were never served at all: half
#      the search space would have waited for classes 0..9 to finish entirely.
#   2. Because of (1), classes 10..19 sat at 8-9 unfinished partitions each
#      while classes 0..9 were worked down, and nothing would have started them
#      until every one of 0..9 was completely finished.
#
# HARD-WON: each shard is TWO processes with the SAME command line, a parent
# (~0.03 CPU-seconds, ~1.1 MB, permanently idle) and the worker that does the
# arithmetic (~23,800 CPU-seconds, 50-250 MB). The idle parent is NOT dead
# weight. Killing the parents on 2026-08-25, on exactly that misreading, took
# down every worker with them (broken pipe) and lost nine in-flight partitions.
# Never kill a shard process because it shows no CPU. Count shard NUMBERS, and
# let a shard's absence from the running set be the only trigger to launch it.

$wd   = "E:\_Temp\caos-research-tau\problems\computation-complexity\tau-conjecture\experiments\EXP-013-additive-residual"
$py   = "D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe"
$N    = 20        # shard count (partition p belongs to shard p mod N)
$want = 20        # how many shards to keep running; 32 cores here, another
                  # session holds 8, so 20 leaves the machine shared but busy

# --- which shard numbers are genuinely running right now? -------------------
$running = @{}
Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -like "*scan9add_fast.py*" } |
    ForEach-Object {
        if ($_.CommandLine -match '--shard\s+(\d+)') { $running[[int]$Matches[1]] = $true }
    }

# --- which shard classes still have unfinished partitions? ------------------
$done = @{}
Get-ChildItem "$wd\artifacts\parts_final\part*.json" -ErrorAction SilentlyContinue | ForEach-Object {
    if ($_.BaseName -match 'part(\d+)') { $done[[int]$Matches[1]] = $true }
}
$needed = 0..($N - 1) | Where-Object {
    $k = $_
    @(0..255 | Where-Object { $_ % $N -eq $k -and -not $done.ContainsKey($_) }).Count -gt 0
}

# --- launch needy shards that are not already running -----------------------
$slots  = $want - $running.Count
$launch = @($needed | Where-Object { -not $running.ContainsKey($_) } | Select-Object -First ([Math]::Max($slots, 0)))

if ($launch.Count -eq 0) {
    "$(Get-Date -Format s) nothing to launch (running: $($running.Keys.Count), needy: $($needed.Count))" |
        Add-Content "$wd\keepalive.log"
    exit 0
}

# Fresh log names per launch: a batch whose append target is locked by a prior
# process fails instantly and silently, which cost a whole launch wave once.
$stamp = Get-Date -Format "MMdd-HHmmss"
foreach ($k in $launch) {
    $tag = "{0:d2}" -f $k
    Start-Process -FilePath $py `
        -ArgumentList "scan9add_fast.py", "--shard", $k, "--nshards", $N `
        -WorkingDirectory $wd -WindowStyle Hidden `
        -RedirectStandardOutput "$wd\logs\sh_${tag}_$stamp.log" `
        -RedirectStandardError  "$wd\logs\sh_${tag}_$stamp.err" | Out-Null
}
"$(Get-Date -Format s) launched $($launch.Count) shards: $($launch -join ',') (was running: $($running.Keys.Count))" |
    Add-Content "$wd\keepalive.log"
