$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "========================================"
Write-Host " ShipGit Basic Regression Test"
Write-Host " ShipGit 基础回归测试"
Write-Host "========================================"

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

Run-Step "Version / 版本: shipgit version" {
    shipgit version
}

Run-Step "Version / 版本: shipgit -v" {
    shipgit -v
}

Run-Step "Version / 版本: shipgit --version" {
    shipgit --version
}

Run-Step "Guide / 指引: shipgit guide" {
    shipgit guide
}

Run-Step "Guide / 指引: shipgit guide --lang en" {
    shipgit guide --lang en
}

Run-Step "Self-test / 自检: shipgit test" {
    shipgit test
}

Run-Step "Self-test / 自检: shipgit test --lang en" {
    shipgit test --lang en
}

Run-Step "Self-test / 自检: shipgit --lang bi test" {
    shipgit --lang bi test
}

Run-Step "Set language / 设置语言: zh with bilingual output" {
    shipgit config-lang zh --lang bi
}

Run-Step "Doctor / 诊断: zh default" {
    shipgit doctor
}

Run-Step "Doctor / 诊断: en command override" {
    shipgit doctor --lang en
}

Run-Step "Doctor / 诊断: bi global override" {
    shipgit --lang bi doctor
}

Run-Step "Status / 状态: zh default" {
    shipgit status
}

Run-Step "Status / 状态: en command override" {
    shipgit status --lang en
}

Run-Step "Status / 状态: bi global override" {
    shipgit --lang bi status
}

Run-Step "Init / 初始化: zh default" {
    shipgit init
}

Run-Step "Init / 初始化: en command override" {
    shipgit init --lang en
}

Run-Step "Remote list / 远程仓库列表: zh default" {
    shipgit config-lang zh --lang bi
    shipgit remote-list
}

Run-Step "Remote list / 远程仓库列表: en command override" {
    shipgit remote-list --lang en
}

Run-Step "Remote list / 远程仓库列表: bi global override" {
    shipgit --lang bi remote-list
}

Write-Host ""
Write-Host "========================================"
Write-Host " ShipGit Basic Regression Test Passed"
Write-Host " ShipGit 基础回归测试通过"
Write-Host "========================================" -ForegroundColor Green
