$ErrorActionPreference = "Stop"

$Root = Join-Path $env:TEMP ("shipgit-test-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $Root | Out-Null

Write-Host ""
Write-Host "========================================"
Write-Host " ShipGit Isolated Regression Test"
Write-Host " ShipGit 隔离回归测试"
Write-Host "========================================"
Write-Host "Test project / 测试项目: $Root" -ForegroundColor Cyan

function Run-Step {
    param(
        [string]$Name,
        [scriptblock]$Command
    )

    Write-Host ""
    Write-Host "---- $Name ----" -ForegroundColor Cyan
    & $Command

    if ($LASTEXITCODE -ne 0) {
        throw "Step failed: $Name"
    }
}

try {
    Push-Location $Root

    "hello shipgit" | Set-Content README.md -Encoding UTF8

    Run-Step "Init / 初始化: shipgit init" {
        shipgit init
    }

    Run-Step "Guide / 指引: shipgit guide --lang bi" {
        shipgit guide --lang bi
    }

    Run-Step "Doctor / 诊断: zh default" {
        shipgit doctor
    }

    Run-Step "Doctor / 诊断: en override" {
        shipgit doctor --lang en
    }

    Run-Step "Doctor / 诊断: bi override" {
        shipgit --lang bi doctor
    }

    Run-Step "Status / 状态: zh default" {
        shipgit status
    }

    Run-Step "Status / 状态: en override" {
        shipgit status --lang en
    }

    Run-Step "Status / 状态: bi override" {
        shipgit --lang bi status
    }

    Run-Step "Remote add / 添加远程仓库: local-test" {
        shipgit remote-add local-test "https://example.com/example/shipgit-test.git"
    }

    Run-Step "Remote list / 远程仓库列表: zh default" {
        shipgit remote-list
    }

    Run-Step "Remote list / 远程仓库列表: en override" {
        shipgit remote-list --lang en
    }

    Run-Step "Remote list / 远程仓库列表: bi override" {
        shipgit --lang bi remote-list
    }

    Run-Step "Verify git remote / 验证 Git 远程仓库" {
        git remote -v
    }

    Run-Step "Config file / 配置文件检查" {
        Get-Content .shipgit.yml
    }

    Write-Host ""
    Write-Host "========================================"
    Write-Host " ShipGit Isolated Regression Test Passed"
    Write-Host " ShipGit 隔离回归测试通过"
    Write-Host "========================================" -ForegroundColor Green
}
finally {
    Pop-Location
    Remove-Item -Recurse -Force $Root
}
