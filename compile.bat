@echo off
REM =============================================================================
REM ПРОСЛОЙКА ДЛЯ ЗАПУСКА MAKE ВНУТРИ DOCKER-КОНТЕЙНЕРА
REM Управляет Docker, передает параметры в Makefile.
REM Использование: .\compile.bat [путь_к_папке] [цель_make] [имя_файла.tex]
REM =============================================================================

chcp 65001 > nul
setlocal EnableDelayedExpansion

REM === КОНФИГУРАЦИЯ ===
set IMAGE_NAME=latex-compiler-env
set CONTAINER_NAME=latex-daemon
set DEFAULT_FILENAME=_report.tex
set BIB_FILE=references.bib

REM === СПЕЦИАЛЬНЫЕ КОМАНДЫ ===
IF "%1"=="stop" (
    echo 🛑 Останавливаю контейнер LaTeX...
    docker stop %CONTAINER_NAME% >nul 2>&1
    docker rm %CONTAINER_NAME% >nul 2>&1
    echo ✅ Контейнер остановлен
    exit /b 0
)
IF "%1"=="status" (
    docker ps | findstr %CONTAINER_NAME% >nul
    IF ERRORLEVEL 1 (
        echo 🔴 Контейнер LaTeX не запущен
    ) ELSE (
        echo 🟢 Контейнер LaTeX работает
    )
    exit /b 0
)

REM === ПРОВЕРКА АРГУМЕНТОВ ===
IF "%1"=="" (
    echo ❌ Ошибка: Укажите путь к папке с работой.
    echo.
    echo Использование: .\compile.bat ^<путь_к_папке^> [цель] [имя_файла.tex]
    echo.
    echo Примеры:
    echo   .\compile.bat reports\physics\lab-1
    echo   .\compile.bat reports\math\sem-2 clean
    echo.
    echo Цели ^(определяются в Makefile^):
    echo   all/pdf  - Полная сборка проекта [по умолчанию: all]
    echo   clean    - Удаление временных файлов
    exit /b 1
)

REM === ПАРАМЕТРЫ ===
set "PROJECT_PATH=%1"
set "MAKE_TARGET=all"
set "TEX_FILE=%DEFAULT_FILENAME%"
IF NOT "%2"=="" set "MAKE_TARGET=%2"
IF NOT "%3"=="" set "TEX_FILE=%3"

REM === ПРОВЕРКА DOCKER ===
docker version >nul 2>&1
IF ERRORLEVEL 1 (
    echo ❌ Docker не запущен или не установлен!
    exit /b 1
)

REM === ПЕРЕСБОРКА ПРИ ИЗМЕНЕНИИ DOCKERFILE ===
set "DOCKERFILE=%cd%\core\Dockerfile"
set "BUILD_CONTEXT=%cd%"
if exist "%DOCKERFILE%" (
    for /f "skip=1 delims=" %%i in ('certutil -hashfile "%DOCKERFILE%" SHA256 ^| findstr /r /v /c:"CertUtil"') do set "DOCKER_HASH=%%i"
    set "DOCKER_HASH=!DOCKER_HASH: =!"
    set "TAG=%IMAGE_NAME%:!DOCKER_HASH:~0,12!"
    docker inspect --type=image !TAG! >nul 2>&1
    if ERRORLEVEL 1 (
        echo 🔨 Изменился Dockerfile. Пересборка образа...
        docker build -f "%DOCKERFILE%" -t !TAG! -t %IMAGE_NAME%:latest "%BUILD_CONTEXT%"
        if ERRORLEVEL 1 (
            echo.
            echo ❌ ОШИБКА СБОРКИ!
            exit /b 1
        )
        docker stop %CONTAINER_NAME% >nul 2>&1
        docker rm %CONTAINER_NAME% >nul 2>&1
    )
    set "IMAGE_TAG=%IMAGE_NAME%:latest"
) else (
    echo ❌ Dockerfile не найден: %DOCKERFILE%
    exit /b 1
)

REM === АВТОМАТИЧЕСКИЙ ЗАПУСК КОНТЕЙНЕРА ===
docker ps | findstr %CONTAINER_NAME% >nul
IF ERRORLEVEL 1 (
    echo 🔧 Контейнер не запущен. Запускаю...
    docker stop %CONTAINER_NAME% >nul 2>&1
    docker rm %CONTAINER_NAME% >nul 2>&1
    echo 📁 Монтирую рабочую директорию: %cd%
    docker run -d --name %CONTAINER_NAME% -v "%cd%":/workdir %IMAGE_TAG% sleep infinity >nul
    echo 🟢 Контейнер запущен
) ELSE (
    echo 🟢 Используется работающий контейнер
)

REM === ПРОВЕРКА ФАЙЛА ===
if not exist "%PROJECT_PATH%\%TEX_FILE%" (
    echo ❌ Файл '%TEX_FILE%' не найден в папке '%PROJECT_PATH%'!
    exit /b 1
)

echo 📁 Проект:  %PROJECT_PATH%
echo 📄 Файл:    %TEX_FILE%
echo 🎯 Цель:   %MAKE_TARGET%
echo.

REM === КОПИРОВАНИЕ ШАБЛОНА ===
echo 📋 Копирую template во временную директорию контейнера...
docker exec %CONTAINER_NAME% bash -c "if [ -d '/workdir/core/templates' ]; then mkdir -p /tmp/latex-template/template && cp -r /workdir/core/templates/* /tmp/latex-template/template && echo '✅ Template скопирован...'; fi" >nul

REM === ГЕНЕРАЦИЯ ИМЕНИ ФАЙЛА (JOBNAME) ===
REM Логика: берем путь, отсекаем всё до sem_X включительно, заменяем слэши на подчеркивания.
REM Пример: reports\sem_3\pioa\kur -> pioa_kur
set "GEN_JOBNAME="
for /f "usebackq delims=" %%I in (`powershell -NoProfile -Command "'%PROJECT_PATH%' -replace '^.*sem_\d+[\\/]', '' -replace '[\\/]', '_' "`) do set "GEN_JOBNAME=%%I"

IF "!GEN_JOBNAME!"=="" (
    echo ⚠️ Не удалось сгенерировать имя из пути. Использую стандартное.
    set "GEN_JOBNAME=!TEX_FILE:.tex=!"
)
echo 🏷️  Имя выходного файла: !GEN_JOBNAME!.pdf

REM === ЗАПУСК MAKE ВНУТРИ КОНТЕЙНЕРА ===
set START_TIME=%TIME%
echo 🚀 Запускаю сборку через Makefile (цель: %MAKE_TARGET%)...
echo.

REM Собираем команду для выполнения внутри Docker
set "TEXLIVE_BIN_PATH=/usr/local/texlive/2025/bin/x86_64-linux"
set "DEFAULT_PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
set "BASH_CMD="
set "BASH_CMD=!BASH_CMD! export PATH=!TEXLIVE_BIN_PATH!:!DEFAULT_PATH! && "
set "BASH_CMD=!BASH_CMD! export TEXINPUTS=.:/tmp/latex-template//:: && "
set "BASH_CMD=!BASH_CMD! make -f /workdir/core/Makefile --always-make %MAKE_TARGET% TEX_FILE='!TEX_FILE!' BIB_FILE='!BIB_FILE!' JOBNAME='!GEN_JOBNAME!'"
docker exec -w "/workdir/%PROJECT_PATH:\=/%" %CONTAINER_NAME% bash -c "!BASH_CMD!"

REM === ПРОВЕРКА РЕЗУЛЬТАТА ===
set END_TIME=%TIME%
set "OUTPUT_DIR=%PROJECT_PATH%\out"
set "PDF_FILE=!GEN_JOBNAME!.pdf"
if exist "%OUTPUT_DIR%\!PDF_FILE!" (
    echo.
    echo ✅ %PDF_FILE%  📁 %PROJECT_PATH%  🎯 %MAKE_TARGET%  ⏱️ %START_TIME% -%END_TIME%
) else (
    echo.
    echo ❌ PDF файл не создан! Проверьте логи Makefile выше.
    exit /b 1
)

endlocal