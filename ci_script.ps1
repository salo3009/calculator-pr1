[file name]: ci_script.ps1
[file content begin]
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

Write-Host "[2/5] Установка зависимостей для сборки..." -ForegroundColor Cyan

pip install pyinstaller
if ($LASTEXITCODE -ne 0) {
    Write-Host "Ошибка: не удалось установить PyInstaller." -ForegroundColor Red
    exit 1
}

if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
    Write-Host "Зависимости из requirements.txt установлены." -ForegroundColor Green
} else {
    Write-Host "Файл requirements.txt не найден, устанавливаем основные зависимости..." -ForegroundColor Yellow
    pip install tk
}

Write-Host "[3/5] Запуск юнит-тестов..." -ForegroundColor Cyan

python -c "import unittest" 2>$null
if ($LASTEXITCODE -eq 0) {
    if (Test-Path "test_calculator.py") {
        python -m pytest test_calculator.py -v
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Тесты провалились!" -ForegroundColor Red
            exit 1
        }
        Write-Host "Все тесты пройдены успешно." -ForegroundColor Green
    } else {
        Write-Host "Файл test_calculator.py не найден, пропускаем тесты." -ForegroundColor Yellow
    }
} else {
    Write-Host "Модуль unittest не найден, пропускаем тесты." -ForegroundColor Yellow
}

Write-Host "[4/5] Сборка исполняемого файла с помощью PyInstaller..." -ForegroundColor Cyan

if (-not (Test-Path "main_app.py")) {
    Write-Host "Ошибка: файл main_app.py не найден!" -ForegroundColor Red
    exit 1
}

$ExeName = "Calculator"

$SpecContent = @"
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main_app.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='$ExeName',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Запуск без консоли (GUI приложение)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
"@

$SpecContent | Out-File -FilePath "calculator_spec.spec" -Encoding UTF8

Write-Host "Запуск PyInstaller для сборки исполняемого файла..." -ForegroundColor Cyan
pyinstaller --onefile --windowed --name "$ExeName" --clean main_app.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Ошибка при сборке с PyInstaller." -ForegroundColor Red
    exit 1
}

$DistDir = "dist"
if (-not (Test-Path $DistDir)) {
    Write-Host "Ошибка: папка dist не создана." -ForegroundColor Red
    exit 1
}

$ExeFile = Get-ChildItem -Path $DistDir -Filter "*.exe" | Select-Object -First 1
if (-not $ExeFile) {
    Write-Host "Ошибка: исполняемый файл не создан." -ForegroundColor Red
    exit 1
}

Write-Host "Исполняемый файл создан: $($ExeFile.FullName)" -ForegroundColor Green
Write-Host "Размер файла: $([math]::Round($ExeFile.Length/1MB, 2)) MB" -ForegroundColor Cyan

Write-Host "[5/5] Создание установочного пакета..." -ForegroundColor Cyan

$PackageDir = "package"
if (Test-Path $PackageDir) {
    Remove-Item -Recurse -Force $PackageDir
}
New-Item -ItemType Directory -Path $PackageDir | Out-Null

Copy-Item -Path $ExeFile.FullName -Destination "$PackageDir\$($ExeFile.Name)"

$ZipFile = "$($ExeName)_v1.0.0.zip"
if (Test-Path $ZipFile) {
    Remove-Item -Force $ZipFile
}

Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory($PackageDir, $ZipFile)

Write-Host "Установочный пакет создан: $ZipFile" -ForegroundColor Green

Write-Host "Очистка временных файлов..." -ForegroundColor Yellow
Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force __pycache__ -ErrorAction SilentlyContinue
Get-ChildItem . -Recurse -Directory -Name "__pycache__" | ForEach-Object {
    $path = Join-Path (Split-Path $_ -Parent) "__pycache__"
    if (Test-Path $path) { Remove-Item -Recurse -Force $path }
}
Remove-Item -Force calculator_spec.spec -ErrorAction SilentlyContinue

Write-Host "[CI] Непрерывная интеграция успешно завершена!" -ForegroundColor Green
Write-Host "Результаты:" -ForegroundColor Cyan
Write-Host "  - Исполняемый файл: $($ExeFile.FullName)" -ForegroundColor Cyan
Write-Host "  - Установочный пакет: $ZipFile" -ForegroundColor Cyan
Write-Host "  - Размер пакета: $([math]::Round((Get-Item $ZipFile).Length/1MB, 2)) MB" -ForegroundColor Cyan
[file content end]
