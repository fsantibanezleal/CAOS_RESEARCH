# Self-healing launcher for the EXP-013 additive shards.
#
# Guard is COMMAND-LINE SPECIFIC on purpose: this machine runs other
# sessions' python work, so "is any python.exe running" is the wrong
# question (and acting on it once cost another session its processes).
# Only our own scan9add_fast.py shards count.

$wd    = "E:\_Temp\caos-research-tau\problems\computation-complexity\tau-conjecture\experiments\EXP-013-additive-residual"
$py    = "D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe"
$N     = 20        # shard count (partitions are taken as p mod N == k)
$want  = 10        # how many shards to keep running (neighbourly share)

$mine = @(Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" -ErrorAction SilentlyContinue |
          Where-Object { $_.CommandLine -like "*scan9add_fast.py*" })

if ($mine.Count -ge 1) { exit 0 }   # already running; nothing to do

# Which shards still have unfinished partitions? Launch only those.
$done = @{}
Get-ChildItem "$wd\artifacts\parts_final\part*.json" -ErrorAction SilentlyContinue | ForEach-Object {
    if ($_.BaseName -match 'part(\d+)') { $done[[int]$Matches[1]] = $true }
}
$needed = 0..($N-1) | Where-Object {
    $k = $_
    @(0..255 | Where-Object { $_ % $N -eq $k -and -not $done.ContainsKey($_) }).Count -gt 0
}

$launch = @($needed | Select-Object -First $want)
foreach ($k in $launch) {
    $tag = "{0:d2}" -f $k
    Start-Process -FilePath $py `
        -ArgumentList "scan9add_fast.py","--shard",$k,"--nshards",$N `
        -WorkingDirectory $wd -WindowStyle Hidden `
        -RedirectStandardOutput "$wd\ka_$tag.log" -RedirectStandardError "$wd\ka_$tag.err" | Out-Null
}
"$(Get-Date -Format s) launched $($launch.Count) shards: $($launch -join ',')" |
    Add-Content "$wd\keepalive.log"
