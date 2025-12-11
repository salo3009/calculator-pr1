param(
    [string]$RepoUrl = "https://github.com/salo3009/calculator-pr1",
    [string]$BuildDir = $PSScriptRoot
)

$RepoUrl = $RepoUrl.Trim()

if (-not $RepoUrl -or -not $BuildDir) {
    Write-Host "Ошибка: не указаны необходимые параметры." -ForegroundColor Red
    exit 1
}

$ProjectName = [System.IO.Path]::GetFileNameWithoutExtension($RepoUrl.TrimEnd('/'))
Write-Host "[CI] Начало непрерывной интеграции для Python-проекта '$ProjectName'" -ForegroundColor Green

Write-Host "[1/5] Загрузка актуальной версии из репозитория..." -ForegroundColor Cyan

if (Test-Path "$BuildDir\.git") {
    Set-Location $BuildDir
    git fetch origin
    git checkout master --quiet
    git reset --hard origin/master --quiet
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Ошибка: не удалось обновиться до origin/master." -ForegroundColor Red
        exit 1
    }
} else {
    if (Test-Path $BuildDir) {
        Remove-Item -Recurse -Force $BuildDir
    }
    git clone $RepoUrl $BuildDir
    if (-not $?) {
        Write-Host "Ошибка: не удалось клонировать репозиторий." -ForegroundColor Red
        exit 1
    }
    Set-Location $BuildDir
}

Write-Host "[2/5] Сборка проекта (python setup.py sdist)..." -ForegroundColor Cyan

if (-not (Test-Path "setup.py")) {
    Write-Host "Ошибка: файл setup.py не найден в корне проекта!" -ForegroundColor Red
    Write-Host ">>> Убедитесь, что в вашем репозитории есть setup.py <<<" -ForegroundColor Yellow
    exit 1
}

Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue
Get-ChildItem . -Recurse -Directory -Name "__pycache__" | ForEach-Object {
    $path = Join-Path (Split-Path $_ -Parent) "__pycache__"
    if (Test-Path $path) { Remove-Item -Recurse -Force $path }
}

python setup.py sdist
if (-not (Test-Path "dist")) {
    Write-Host "Ошибка: не удалось создать дистрибутив (папка dist отсутствует)." -ForegroundColor Red
    exit 1
}

Write-Host "Сборка завершена. Архив: $(Get-ChildItem dist)" -ForegroundColor Green

Write-Host "[3/5] Запуск юнит-тестов..." -ForegroundColor Cyan

python -m unittest discover -s test_calculator
if ($LASTEXITCODE -ne 0) {
    Write-Host "Тесты провалились!" -ForegroundColor Red
    exit 1
}

Write-Host "Все тесты пройдены успешно." -ForegroundColor Green

Write-Host "[4/5] Установочный архив создан: $(Get-ChildItem dist)" -ForegroundColor Cyan

Write-Host "[5/5] Установка приложения через pip..." -ForegroundColor Cyan

pip install .

Write-Host "[CI] Непрерывная интеграция успешно завершена!" -ForegroundColor Green