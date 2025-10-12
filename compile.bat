@echo off
REM Скрипт для компиляции LaTeX-проекта с помощью Docker.
REM Использование: .\compile.bat <путь_к_папке> [имя_файла.tex]

chcp 65001 > nul

IF "%1"=="" (
    echo Ошибка: Укажите путь к папке с работой.
    echo Пример: .\compile.bat reports\sem_3\physics\lab-2
    exit /b 1
)

set FILENAME=_report.tex
IF NOT "%2"=="" (
    set FILENAME=%2
)

REM --- АВТОМАТИЧЕСКАЯ ОЧИСТКА ---
echo Очищаю временные файлы в папке %1...
del /Q "%1\*.aux" >nul 2>nul
del /Q "%1\*.log" >nul 2>nul
del /Q "%1\*.out" >nul 2>nul
del /Q "%1\*.toc" >nul 2>nul
del /Q "%1\*.fls" >nul 2>nul
del /Q "%1\*.fdb_latexmk" >nul 2>nul
REM --- КОНЕЦ БЛОКА ОЧИСТКИ ---

set IMAGE_NAME=latex-compiler-env
docker inspect --type=image %IMAGE_NAME% > nul 2>nul
IF errorlevel 1 (
    echo Образ %IMAGE_NAME% не найден. Начинаю сборку...
    docker build -t %IMAGE_NAME% .
)

set "DOCKER_PATH=%1"
set "DOCKER_PATH=%DOCKER_PATH:\=/%"

echo Запускаю компиляцию файла %FILENAME% в папке: %DOCKER_PATH%

docker run --rm ^
    -v "%cd%":/workdir ^
    -e "TEXINPUTS=/workdir//:" ^
    -w /workdir/%DOCKER_PATH% ^
    %IMAGE_NAME% lualatex -interaction=batchmode %FILENAME%

echo Компиляция завершена. PDF-файл должен находиться в папке %1. Если его там нет, см. .log файл для нахождения ошибок (в терминале они не печатаются).