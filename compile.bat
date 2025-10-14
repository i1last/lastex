@echo off
REM =============================================================================
REM УМНЫЙ СКРИПТ КОМПИЛЯЦИИ LaTeX С АВТОМАТИЧЕСКИМ УПРАВЛЕНИЕМ КОНТЕЙНЕРОМ
REM Использование: .\compile.bat [путь_к_папке] [имя_файла.tex] [режим]
REM Режимы: fast (черновик), full (финальный), stop (остановить контейнер)
REM =============================================================================

chcp 65001 > nul
setlocal EnableDelayedExpansion





REM === КОНФИГУРАЦИЯ ===
set IMAGE_NAME=latex-compiler-env
set CONTAINER_NAME=latex-daemon
set DEFAULT_FILENAME=_report.tex





REM === СПЕЦИАЛЬНЫЕ КОМАНДЫ ===
IF "%1"=="stop" (
    echo 🛑 Останавливаю контейнер LaTeX...
    docker stop %CONTAINER_NAME% 2>nul
    docker rm %CONTAINER_NAME% 2>nul
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
    echo Использование: .\compile.bat ^<путь_к_папке^> [режим] [имя_файла.tex]
    echo.
    echo Примеры:
    echo   .\compile.bat reports\physics\lab-1
    echo   .\compile.bat reports\math\sem-2 main.tex full
    echo   .\compile.bat stop                    - остановить фоновый контейнер
    echo   .\compile.bat status                  - статус контейнера
    echo.
    echo Режимы:
    echo   fast  - черновая компиляция [быстро]
    echo   full  - полная компиляция [с SyncTeX] [по умолчанию]
    exit /b 1
)





REM === ПАРАМЕТРЫ ===
set "PROJECT_PATH=%1"
set "TEX_FILE=%DEFAULT_FILENAME%"
set "COMPILE_MODE=full"

IF NOT "%2"=="" set "COMPILE_MODE=%2"
IF NOT "%3"=="" set "TEX_FILE=%3"

REM === ПОДГОТОВКА ПУТЕЙ ===
set "DOCKER_PATH=%PROJECT_PATH:\=/%"
set "OUTPUT_DIR=%PROJECT_PATH%\out"





REM === ПРОВЕРКА DOCKER ===
docker version >nul 2>&1
IF ERRORLEVEL 1 (
    echo ❌ Docker не запущен или не установлен!
    exit /b 1
)





REM === ПРОВЕРКА ОБРАЗА ===
docker inspect --type=image %IMAGE_NAME% >nul 2>&1
IF ERRORLEVEL 1 (
    echo 🔧 Образ %IMAGE_NAME% не найден. Сборка...
    docker build -t %IMAGE_NAME% . || (
        echo ❌ Ошибка сборки образа!
        exit /b 1
    )
)





REM === АВТОМАТИЧЕСКИЙ ЗАПУСК КОНТЕЙНЕРА ===
docker ps | findstr %CONTAINER_NAME% >nul
IF ERRORLEVEL 1 (
    echo 🔧 Контейнер не запущен. Запускаю...
    docker stop %CONTAINER_NAME% 2>nul
    docker rm %CONTAINER_NAME% 2>nul

    echo 📁 Монтирую рабочую директорию: %cd%
    docker run -d --name %CONTAINER_NAME% ^
        -v "%cd%":/workdir ^
        -w /workdir ^
        %IMAGE_NAME% ^
        sleep infinity
    echo 🟢 Контейнер запущен
) ELSE (
    echo 🟢 Используется работающий контейнер
)





REM === ПРОВЕРКА ФАЙЛА ===
if not exist "%PROJECT_PATH%\%TEX_FILE%" (
    echo ❌ Файл '%TEX_FILE%' не найден в папке '%PROJECT_PATH%'!
    echo.
    echo Найденные .tex файлы:
    dir /b "%PROJECT_PATH%\*.tex" 2>nul || echo    - нет .tex файлов
    exit /b 1
)

echo 📁 Проект:  %PROJECT_PATH%
echo 📄 Файл:    %TEX_FILE%
echo 🎯 Режим:   %COMPILE_MODE%
echo 📂 Выход:   %OUTPUT_DIR%
echo.





REM === СОЗДАНИЕ ВЫХОДНОЙ ДИРЕКТОРИИ ===
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"





REM === КОМАНДЫ КОМПИЛЯЦИИ ===
set "COMPILE_CMD="
set "LATEX_OPTS=-output-directory=out -interaction=nonstopmode"

IF "%COMPILE_MODE%"=="fast" (
    echo ⚡ ЧЕРНОВАЯ КОМПИЛЯЦИЯ...
    set "COMPILE_CMD=lualatex %LATEX_OPTS% %TEX_FILE%"
)

IF "%COMPILE_MODE%"=="full" (
    echo 🔧 ПОЛНАЯ КОМПИЛЯЦИЯ...
    set "COMPILE_CMD=lualatex %LATEX_OPTS% -synctex=1 %TEX_FILE%"
)

if "!COMPILE_CMD!"=="" (
    echo ❌ Неизвестный режим: %COMPILE_MODE%
    echo 💡 Доступные режимы: fast, full
    exit /b 1
)





REM === КОПИРОВАНИЕ ПАПКИ TEMPLATE ВО ВРЕМЕННУЮ ДИРЕКТОРИЮ КОНТЕЙНЕРА ===
echo 📋 Копирую template во временную директорию контейнера...
docker exec %CONTAINER_NAME% bash -c "if [ -d '/workdir/template' ]; then mkdir -p /tmp/latex-template/template && cp -r /workdir/template/* /tmp/latex-template/template && echo '✅ Template скопирован во временную директорию'; else echo '❌ Папка template не найдена в корне'; fi"





REM === ЗАПУСК КОМПИЛЯЦИИ С ПРАВИЛЬНЫМИ ПУТЯМИ ===
set START_TIME=%TIME%

echo 🔄 Компилирую...
docker exec -e "TEXINPUTS=.:/tmp/latex-template//:" -w "/workdir/%DOCKER_PATH%" %CONTAINER_NAME% bash -c "!COMPILE_CMD!"





REM === ПРОВЕРКА РЕЗУЛЬТАТА ===
set PDF_FILE=%TEX_FILE:.tex=.pdf%
set END_TIME=%TIME%

echo 📁 Проект:  %PROJECT_PATH%
echo 📄 Файл:    %TEX_FILE%
echo 🎯 Режим:   %COMPILE_MODE%
echo 📂 Выход:   %OUTPUT_DIR%
echo.

if exist "%OUTPUT_DIR%\%PDF_FILE%" (    
    echo ✅ КОМПИЛЯЦИЯ УСПЕШНА
    echo 📊 Файл: %OUTPUT_DIR%\%PDF_FILE%
    echo ⏱️ Время: %START_TIME% - %END_TIME%
    echo.
) else (
    echo ❌ PDF файл не создан!
    echo.
    echo 🔍 Проверьте:
    echo   - Синтаксис LaTeX в файле
    echo   - Логи компиляции
    exit /b 1
)

endlocal