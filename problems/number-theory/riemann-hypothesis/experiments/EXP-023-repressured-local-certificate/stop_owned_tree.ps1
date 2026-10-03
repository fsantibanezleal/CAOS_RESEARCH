param(
    [Parameter(Mandatory=$true)][int]$RootPid,
    [Parameter(Mandatory=$true)][long]$RootStartedTicks,
    [Parameter(Mandatory=$true)][string]$CommandToken
)
$ErrorActionPreference = 'Stop'
$rootProcess = Get-Process -Id $RootPid -ErrorAction SilentlyContinue
if ($null -eq $rootProcess) { Write-Output '{"root_exited":true,"stopped":[]}'; exit 0 }
if ($rootProcess.StartTime.ToUniversalTime().Ticks -ne $RootStartedTicks) { throw 'Root PID was reused' }
$all = @(Get-CimInstance Win32_Process)
$rootInfo = $all | Where-Object ProcessId -eq $RootPid
if ($null -eq $rootInfo -or $null -eq $rootInfo.CommandLine -or
    $rootInfo.CommandLine.IndexOf($CommandToken,[StringComparison]::OrdinalIgnoreCase) -lt 0) {
    throw 'Root command identity mismatch'
}
$owned = [System.Collections.Generic.List[object]]::new()
$owned.Add([pscustomobject]@{Pid=$RootPid; Created=$rootInfo.CreationDate; Depth=0; Ticks=$RootStartedTicks})
for ($i=0; $i -lt $owned.Count; $i++) {
    $parent = $owned[$i]
    foreach ($child in @($all | Where-Object ParentProcessId -eq $parent.Pid)) {
        if ($child.CreationDate -lt $parent.Created) { continue }
        if (@($owned | Where-Object Pid -eq $child.ProcessId).Count -ne 0) { continue }
        $process = Get-Process -Id $child.ProcessId -ErrorAction SilentlyContinue
        if ($null -ne $process) {
            if ([Math]::Abs($process.StartTime.ToUniversalTime().Ticks -
                $child.CreationDate.ToUniversalTime().Ticks) -gt 10) {
                throw 'Descendant changed identity during capture'
            }
            $owned.Add([pscustomobject]@{Pid=[int]$child.ProcessId; Created=$child.CreationDate;
                Depth=$parent.Depth+1; Ticks=$process.StartTime.ToUniversalTime().Ticks})
        }
    }
}
$stopped = [System.Collections.Generic.List[int]]::new()
$alreadyExited = [System.Collections.Generic.List[int]]::new()
foreach ($item in @($owned | Sort-Object Depth -Descending)) {
    $process = Get-Process -Id $item.Pid -ErrorAction SilentlyContinue
    if ($null -ne $process -and $process.StartTime.ToUniversalTime().Ticks -eq $item.Ticks) {
        try {
            Stop-Process -Id $item.Pid -Force -ErrorAction Stop
            $stopped.Add($item.Pid)
        } catch {
            if ($null -ne (Get-Process -Id $item.Pid -ErrorAction SilentlyContinue)) { throw }
            $alreadyExited.Add($item.Pid)
        }
    } elseif ($null -eq $process) {
        $alreadyExited.Add($item.Pid)
    } else {
        throw 'A captured descendant PID was reused; refusing to stop it'
    }
}
[pscustomobject]@{root_exited=$false; stopped=@($stopped); already_exited=@($alreadyExited)} | ConvertTo-Json -Compress
