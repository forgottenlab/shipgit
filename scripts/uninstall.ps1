param(
    [switch]$Yes
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

function Test-PythonModule {
    param(
        [string]$PythonCommand,
        [string]$ModuleName
    )

    & $PythonCommand -m $ModuleName --version *> $null
    return $LASTEXITCODE -eq 0
}

Write-Host ""
Write-Host "========================================"
Write-Host " ShipGit Uninstaller"
Write-Host " ShipGit 卸载程序"
Write-Host "========================================"

Write-Host "This script will uninstall ShipGit installed by pipx."
Write-Host "此脚本将卸载通过 pipx 安装的 ShipGit。"
Write-Host ""
Write-Host "It will not delete your Git repositories or project files."
Write-Host "它不会删除你的 Git 仓库或项目文件。"
Write-Host ""

$PythonCommand = Resolve-PythonCommand

if ($null -eq $PythonCommand) {
    Write-Host "Python was not found. Cannot run pipx uninstall." -ForegroundColor Yellow
    Write-Host "未找到 Python，无法执行 pipx 卸载。"
    exit 0
}

Write-Host "Python command / Python 命令: $PythonCommand" -ForegroundColor Green

$PipxAvailable = Test-PythonModule $PythonCommand "pipx"

if (-not $PipxAvailable) {
    Write-Host "pipx is not installed. Nothing to uninstall through pipx." -ForegroundColor Yellow
    Write-Host "未检测到 pipx，因此没有可通过 pipx 卸载的 ShipGit。"
    exit 0
}

if (-not $Yes) {
    $answer = Read-Host "Continue? / 是否继续？(y/N)"
    if ($answer -notin @("y", "Y", "yes", "YES")) {
        Write-Host "Cancelled / 已取消。"
        exit 0
    }
}

# Important:
# 当前项目根目录下存在 shipgit/ 源码目录。
# 如果直接在项目根目录运行 `pipx uninstall shipgit`，
# pipx 可能会把 shipgit 识别成路径，而不是包名。
# 所以这里切换到 TEMP 目录执行卸载。
$originalLocation = Get-Location
try {
    Set-Location $env:TEMP
    Invoke-External $PythonCommand @("-m", "pipx", "uninstall", "shipgit") -AllowFailure
}
finally {
    Set-Location $originalLocation
}

Write-Host ""
Write-Host "Checking pipx list / 正在检查 pipx 列表..."

$List = & $PythonCommand -m pipx list

if ($List -match "shipgit") {
    Write-Host "ShipGit still appears in pipx list. Please check manually." -ForegroundColor Yellow
    Write-Host "ShipGit 仍然出现在 pipx 列表中，请手动检查。"
}
else {
    Write-Host "ShipGit has been removed from pipx list." -ForegroundColor Green
    Write-Host "ShipGit 已从 pipx 列表中移除。"
}

Write-Host ""
Write-Host "Uninstall finished / 卸载流程结束。" -ForegroundColor Green
