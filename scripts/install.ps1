param(
    [string]$InstallSource = "git+https://github.com/forgottenlab/shipgit.git",
    [switch]$SkipSelfTest
)

$ErrorActionPreference = "Stop"

$InstallerVersion = "0.1.3"
$RepoHome = "https://github.com/forgottenlab/shipgit"

function Write-Section {
    param([string]$Title)
    Write-Host ""
    Write-Host "========================================" -ForegroundColor DarkGray
    Write-Host " $Title" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor DarkGray
}

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

function Test-PythonModule {
    param(
        [string]$PythonCommand,
        [string]$ModuleName
    )

    & $PythonCommand -m $ModuleName --version *> $null
    return $LASTEXITCODE -eq 0
}

function Get-ShipGitCommand {
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

Write-Section "ShipGit Installer / ShipGit 安装程序"

Write-Host "Installer Version / 安装器版本: $InstallerVersion"
Write-Host "Project / 项目地址: $RepoHome"
Write-Host "Install Source / 安装来源: $InstallSource"
Write-Host ""
Write-Host "Privacy / 隐私说明:" -ForegroundColor Yellow
Write-Host "- ShipGit does not collect machine IDs, tokens, SSH private keys, or personal files."
Write-Host "- ShipGit 不收集机器码、Token、SSH 私钥或用户个人文件。"
Write-Host ""
Write-Host "This script will / 此脚本将会："
Write-Host "1. Check Python / 检查 Python"
Write-Host "2. Check Git / 检查 Git"
Write-Host "3. Install pipx if missing / 如果缺少 pipx 则安装"
Write-Host "4. Install or update ShipGit with pipx / 使用 pipx 安装或更新 ShipGit"
Write-Host "5. Verify the shipgit command / 验证 shipgit 命令"

Write-Section "Checking Python / 检查 Python"

$PythonCommand = Resolve-PythonCommand

if ($null -eq $PythonCommand) {
    Write-Host "Python was not found." -ForegroundColor Red
    Write-Host "未找到 Python。请先安装 Python 3.9+，或确认 conda/python 已加入 PATH。"
    Write-Host "Download / 下载地址: https://www.python.org/downloads/"
    exit 1
}

Write-Host "Python command / Python 命令: $PythonCommand" -ForegroundColor Green
Invoke-External $PythonCommand @("--version")

Write-Section "Checking Git / 检查 Git"

if (-not (Test-Command "git")) {
    Write-Host "Git was not found." -ForegroundColor Red
    Write-Host "未找到 Git。请先安装 Git for Windows。"
    Write-Host "Download / 下载地址: https://git-scm.com/download/win"
    exit 1
}

Write-Host "Detected / 已检测到: $(git --version)" -ForegroundColor Green

Write-Section "Checking pipx / 检查 pipx"

$PipxAvailable = Test-PythonModule $PythonCommand "pipx"

if (-not $PipxAvailable) {
    Write-Host "pipx not found. Installing pipx..." -ForegroundColor Yellow
    Write-Host "未检测到 pipx，正在安装 pipx..." -ForegroundColor Yellow

    Invoke-External $PythonCommand @("-m", "pip", "install", "--user", "pipx")
    Invoke-External $PythonCommand @("-m", "pipx", "ensurepath")
}
else {
    $PipxVersion = & $PythonCommand -m pipx --version
    Write-Host "pipx is available / pipx 已可用: $PipxVersion" -ForegroundColor Green
}

Write-Section "Installing or Updating ShipGit / 安装或更新 ShipGit"

Write-Host "Running / 正在执行:"
Write-Host "$PythonCommand -m pipx install --force $InstallSource"
Write-Host ""

Invoke-External $PythonCommand @("-m", "pipx", "install", "--force", $InstallSource)

Write-Section "Verifying Installation / 验证安装"

$ShipGitCommand = Get-ShipGitCommand

if ($null -eq $ShipGitCommand) {
    Write-Host "ShipGit was installed, but 'shipgit' is not available in this PowerShell session." -ForegroundColor Yellow
    Write-Host "ShipGit 可能已经安装成功，但当前 PowerShell 会话暂时找不到 shipgit 命令。"
    Write-Host ""
    Write-Host "Please restart PowerShell, then run / 请重启 PowerShell 后运行："
    Write-Host "  shipgit -v"
    Write-Host "  shipgit guide"
    Write-Host "  shipgit test"
}
else {
    Write-Host "shipgit command found / 已找到 shipgit 命令：" -ForegroundColor Green
    Write-Host "  $ShipGitCommand"
    Write-Host ""
    & $ShipGitCommand -v

    if (-not $SkipSelfTest) {
        Write-Host ""
        Write-Host "Running self-test / 正在运行自检测试..." -ForegroundColor Cyan
        & $ShipGitCommand test
        if ($LASTEXITCODE -ne 0) {
            throw "ShipGit self-test failed."
        }
    }
}

Write-Section "Next Steps / 下一步"

Write-Host "Run quick guide / 查看基础指引："
Write-Host "  shipgit guide"
Write-Host ""
Write-Host "Run self-test / 运行自检测试："
Write-Host "  shipgit test"
Write-Host ""
Write-Host "Update ShipGit / 更新 ShipGit："
Write-Host "  irm https://raw.githubusercontent.com/forgottenlab/shipgit/main/scripts/install.ps1 | iex"
Write-Host ""
Write-Host "Uninstall ShipGit / 卸载 ShipGit："
Write-Host "  $PythonCommand -m pipx uninstall shipgit"
Write-Host "  或运行 scripts/uninstall.ps1"
Write-Host ""
Write-Host "Safer install / 更安全的安装方式："
Write-Host "  irm https://raw.githubusercontent.com/forgottenlab/shipgit/main/scripts/install.ps1 -OutFile install.ps1"
Write-Host "  Get-Content .\install.ps1"
Write-Host "  .\install.ps1"

Write-Host ""
Write-Host "ShipGit installation finished / ShipGit 安装流程结束" -ForegroundColor Green
