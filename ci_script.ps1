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
    try {
        git fetch origin
        git checkout master --quiet
        git reset --hard origin/master --quiet
    } catch {
        Write-Host "Ошибка: не удалось обновиться до origin/master." -ForegroundColor Red
        exit 1
    }
} else {
    if (Test-Path $BuildDir) {
        Remove-Item -Recurse -Force $BuildDir -ErrorAction SilentlyContinue
    }
    try {
        git clone $RepoUrl $BuildDir
    } catch {
        Write-Host "Ошибка: не удалось клонировать репозиторий." -ForegroundColor Red
        exit 1
    }
    Set-Location $BuildDir
}

Write-Host "[2/5] Установка зависимостей для сборки..." -ForegroundColor Cyan

$pythonCommand = "python"
if (-not (Get-Command $pythonCommand -ErrorAction SilentlyContinue)) {
    $pythonCommand = "python3"
    if (-not (Get-Command $pythonCommand -ErrorAction SilentlyContinue)) {
        Write-Host "Ошибка: Python не найден! Установите Python и добавьте его в PATH." -ForegroundColor Red
        exit 1
    }
}

Write-Host "Используется Python: $pythonCommand" -ForegroundColor Gray

try {
    & $pythonCommand -m pip install --upgrade pip
    & $pythonCommand -m pip install pyinstaller
} catch {
    Write-Host "Ошибка: не удалось установить PyInstaller." -ForegroundColor Red
    exit 1
}

Write-Host "PyInstaller успешно установлен" -ForegroundColor Green

if (Test-Path "requirements.txt") {
    try {
        & $pythonCommand -m pip install -r requirements.txt
        Write-Host "Зависимости из requirements.txt установлены." -ForegroundColor Green
    } catch {
        Write-Host "Предупреждение: не удалось установить зависимости из requirements.txt" -ForegroundColor Yellow
    }
} else {
    Write-Host "Файл requirements.txt не найден, проверяем наличие tkinter..." -ForegroundColor Yellow
    try {
        & $pythonCommand -c "import tkinter" 2>$null
        Write-Host "Tkinter уже установлен" -ForegroundColor Green
    } catch {
        Write-Host "Tkinter не найден, устанавливаем..." -ForegroundColor Yellow
        try {
            & $pythonCommand -m pip install tk
        } catch {
            Write-Host "Предупреждение: не удалось установить tkinter" -ForegroundColor Yellow
        }
    }
}

Write-Host "[3/5] Запуск юнит-тестов..." -ForegroundColor Cyan

if (Test-Path "test_calculator.py") {
    Write-Host "Запуск тестов..." -ForegroundColor Cyan
    try {
        & $pythonCommand test_calculator.py
        Write-Host "Все тесты пройдены успешно." -ForegroundColor Green
    } catch {
        Write-Host "Тесты провалились!" -ForegroundColor Red
        Write-Host "Повторный запуск с подробным выводом..." -ForegroundColor Yellow
        & $pythonCommand test_calculator.py -v
        exit 1
    }
} else {
    Write-Host "Файл test_calculator.py не найден, пропускаем тесты." -ForegroundColor Yellow
}

Write-Host "[4/5] Сборка исполняемого файла с помощью PyInstaller..." -ForegroundColor Cyan

if (-not (Test-Path "main_app.py")) {
    Write-Host "Ошибка: файл main_app.py не найден!" -ForegroundColor Red
    exit 1
}

$requiredFiles = @(
    "basic_operations.py",
    "advanced_operations.py", 
    "scientific_operations.py",
    "memory_operations.py",
    "main_app.py"
)

foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        Write-Host "Ошибка: файл $file не найден!" -ForegroundColor Red
        exit 1
    }
}

$ExeName = "Calculator"

Write-Host "Запуск PyInstaller для сборки исполняемого файла..." -ForegroundColor Cyan

try {
    & $pythonCommand -m PyInstaller --onefile --windowed --name "$ExeName" --clean main_app.py
} catch {
    Write-Host "Ошибка при сборке с PyInstaller: $_" -ForegroundColor Red
    exit 1
}

$DistDir = "dist"
if (-not (Test-Path $DistDir)) {
    Write-Host "Ошибка: папка dist не создана." -ForegroundColor Red
    exit 1
}

$ExeFile = Get-ChildItem -Path $DistDir -Filter "*.exe" | Select-Object -First 1
if (-not $ExeFile) {
    $ExeFile = Get-ChildItem -Path $DistDir -Filter "$ExeName.exe" | Select-Object -First 1
}

if (-not $ExeFile) {
    Write-Host "Ошибка: исполняемый файл не создан." -ForegroundColor Red
    Write-Host "Содержимое папки dist:" -ForegroundColor Yellow
    Get-ChildItem -Path $DistDir | Format-Table Name, Length, LastWriteTime
    exit 1
}

Write-Host "Исполняемый файл создан: $($ExeFile.FullName)" -ForegroundColor Green
Write-Host "Размер файла: $([math]::Round($ExeFile.Length/1MB, 2)) MB" -ForegroundColor Cyan

Write-Host "[5/5] Создание установочного пакета..." -ForegroundColor Cyan

$PackageDir = "package"
if (Test-Path $PackageDir) {
    Remove-Item -Recurse -Force $PackageDir -ErrorAction SilentlyContinue
}
New-Item -ItemType Directory -Path $PackageDir | Out-Null

Copy-Item -Path $ExeFile.FullName -Destination "$PackageDir\$($ExeFile.Name)" -Force

$ZipFile = "$($ExeName)_v1.0.0_$(Get-Date -Format 'yyyyMMdd_HHmmss').zip"
if (Test-Path $ZipFile) {
    Remove-Item -Force $ZipFile -ErrorAction SilentlyContinue
}

# Используем Compress-Archive (доступно в PowerShell 5+)
try {
    Compress-Archive -Path "$PackageDir\*" -DestinationPath $ZipFile -Force
    Write-Host "Установочный пакет создан: $ZipFile" -ForegroundColor Green
    Write-Host "Размер пакета: $([math]::Round((Get-Item $ZipFile).Length/1MB, 2)) MB" -ForegroundColor Cyan
} catch {
    Write-Host "Предупреждение: не удалось создать zip-архив: $_" -ForegroundColor Yellow
    Write-Host "Пакет доступен в папке: $PackageDir" -ForegroundColor Cyan
    $ZipFile = $null
}

Write-Host "Очистка временных файлов..." -ForegroundColor Yellow
Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force __pycache__ -ErrorAction SilentlyContinue
Get-ChildItem . -Recurse -Directory -Name "__pycache__" | ForEach-Object {
    $path = Join-Path (Split-Path $_ -Parent) "__pycache__"
    if (Test-Path $path) { Remove-Item -Recurse -Force $path -ErrorAction SilentlyContinue }
}

Write-Host "[CI] Непрерывная интеграция успешно завершена!" -ForegroundColor Green
