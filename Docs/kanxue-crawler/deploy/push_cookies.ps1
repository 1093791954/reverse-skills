# PowerShell 版的 cookies 同步脚本。Windows 原生跑。
#
# 用法：
#   .\deploy\push_cookies.ps1 -Host kanxue-vps
#   .\deploy\push_cookies.ps1 -Host user@vps.example.com -RemoteRoot /opt/kanxue-crawler

param(
    [Parameter(Mandatory=$true)] [string]$RemoteHost,
    [string]$RemoteRoot = "/opt/kanxue-crawler"
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$LocalFile = Join-Path $ScriptDir "..\state\cookies.json"

if (-not (Test-Path $LocalFile)) {
    Write-Error "local cookies file missing: $LocalFile"
}

Write-Host "[1/3] uploading cookies to ${RemoteHost}:$RemoteRoot/state/cookies.json"
scp $LocalFile "${RemoteHost}:$RemoteRoot/state/cookies.json"
if ($LASTEXITCODE -ne 0) { throw "scp failed" }

Write-Host "[2/3] fixing permissions on remote"
ssh $RemoteHost "sudo chown kanxue:kanxue '$RemoteRoot/state/cookies.json' && sudo chmod 600 '$RemoteRoot/state/cookies.json'"
if ($LASTEXITCODE -ne 0) { throw "remote chown/chmod failed" }

Write-Host "[3/3] verifying login on remote"
ssh $RemoteHost "sudo -u kanxue bash -c 'cd $RemoteRoot && .venv/bin/python -m src.check_login'"
if ($LASTEXITCODE -ne 0) { throw "remote check_login failed" }

Write-Host "OK. cookies pushed and verified." -ForegroundColor Green
