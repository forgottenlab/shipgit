param(
    [switch]$Yes,
    [switch]$LocalSource
)

$ErrorActionPreference = "Stop"

function Test-Command {
    param([string]$Name)
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Resolve-PythonCommand {
    if (Test-Command "py") {
        return "py"
    }

    if (Test-Command "python") {
        return "python"
    }

    return $null
}

function Invoke-External {
    param(
        [string]$FilePath,
        [string[]]$Arguments,
        [switch]$AllowFailure
    )

    & $FilePath @Arguments
    $code = $LASTEXITCODE

    if ($code -ne 0 -and -not $AllowFailure) {
        throw "Command failed with exit code ${code}: $FilePath $($Arguments -join ' ')"
    }
}

function Resolve-ShipGitCommand {
    $candidate = Join-Path $env:USERPROFILE ".local\bin\shipgit.exe"
    if (Test-Path $candidate) {
        return $candidate
    }

    $cmd = Get-Command "shipgit" -ErrorAction SilentlyContinue
    if ($null -ne $cmd) {
        return $cmd.Source
    }

    return $null
}

Write-Host ""
Write-Host "========================================"
Write-Host " ShipGit Distribution Test"
Write-Host " ShipGit 分发安装测试"
Write-Host "========================================"

if ($env:CONDA_DEFAULT_ENV) {
    Write-Host ""
    Write-Host "Warning / 警告：" -ForegroundColor Yellow
    Write-Host "Current Conda environment / 当前 Conda 环境: $env:CONDA_DEFAULT_ENV"
    Write-Host "For a cleaner distribution test, run this script in a fresh PowerShell without conda activation."
    Write-Host "为了更干净地测试分发安装，建议在未激活 conda 的全新 PowerShell 中运行。"
}

$PythonCommand = Resolve-PythonCommand
if ($null -eq $PythonCommand) {
    Write-Host "Python was not found." -ForegroundColor Red
    Write-Host "未找到 Python。请先安装 Python 或确认 python/py 可用。"
    exit 1
}

Write-Host "Python command / Python 命令: $PythonCommand" -ForegroundColor Green
Invoke-External $PythonCommand @("--version")

$InstallSource = "git+https://github.com/forgottenlab/shipgit.git"

if ($LocalSource) {
    $InstallSource = (Resolve-Path ".").Path
}

Write-Host ""
Write-Host "Install Source / 安装来源: $InstallSource" -ForegroundColor Cyan

if (-not $Yes) {
    Write-Host ""
    Write-Host "This test will install, update, and uninstall ShipGit via pipx."
    Write-Host "此测试会通过 pipx 安装、更新并卸载 ShipGit。"
    $answer = Read-Host "Continue? / 是否继续？(y/N)"
    if ($answer -notin @("y", "Y", "yes", "YES")) {
        Write-Host "Cancelled / 已取消。"
        exit 0
    }
}

Write-Host ""
Write-Host "---- Cleanup before test / 测试前清理 ----" -ForegroundColor Cyan
& ".\scripts\uninstall.ps1" -Yes

Write-Host ""
Write-Host "---- Install test / 安装测试 ----" -ForegroundColor Cyan
& ".\scripts\install.ps1" -InstallSource $InstallSource -SkipSelfTest

$ShipGit = Resolve-ShipGitCommand
if ($null -eq $ShipGit) {
    throw "shipgit command not found after install."
}

& $ShipGit -v
if ($LASTEXITCODE -ne 0) { throw "shipgit -v failed." }

& $ShipGit guide --lang en
if ($LASTEXITCODE -ne 0) { throw "shipgit guide failed." }

& $ShipGit test --lang en
if ($LASTEXITCODE -ne 0) { throw "shipgit test failed." }

Write-Host ""
Write-Host "---- Update test / 更新测试 ----" -ForegroundColor Cyan
& ".\scripts\update.ps1" -InstallSource $InstallSource -SkipSelfTest

$ShipGit = Resolve-ShipGitCommand
if ($null -eq $ShipGit) {
    throw "shipgit command not found after update."
}

& $ShipGit -v
if ($LASTEXITCODE -ne 0) { throw "shipgit -v failed after update." }

& $ShipGit test --lang en
if ($LASTEXITCODE -ne 0) { throw "shipgit test failed after update." }

Write-Host ""
Write-Host "---- Uninstall test / 卸载测试 ----" -ForegroundColor Cyan
& ".\scripts\uninstall.ps1" -Yes

Write-Host ""
Write-Host "---- Verify uninstall / 验证卸载 ----" -ForegroundColor Cyan
$PipxList = & $PythonCommand -m pipx list
if ($PipxList -match "shipgit") {
    throw "shipgit still appears in pipx list after uninstall."
}

Write-Host ""
Write-Host "========================================"
Write-Host " ShipGit Distribution Test Passed"
Write-Host " ShipGit 分发安装测试通过"
Write-Host "========================================" -ForegroundColor Green
