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

set IMAGE_NAME=latex-compiler-env
docker inspect --type=image %IMAGE_NAME% > nul 2>nul
IF errorlevel 1 (
    echo Образ %IMAGE_NAME% не найден. Начинаю сборку...
    docker build -t %IMAGE_NAME% .
)

set "DOCKER_PATH=%1"
set "DOCKER_PATH=%DOCKER_PATH:\=/%"

REM === ГАРАНТИРОВАННАЯ ОЧИСТКА ПЕРЕД КОМПИЛЯЦИЕЙ
echo Очистка целевой папки: %1\out\
IF EXIST "%1\out" (
    rmdir /s /q "%1\out"
)
mkdir "%1\out"

echo Запускаю компиляцию файла %FILENAME% в папке: %DOCKER_PATH%

REM === ЗАПУСК КОНТЕЙНЕРА СО СТРОГОЙ ИЗОЛЯЦИЕЙ ПУТЕЙ
docker run --rm ^
    -v "%cd%":/workdir ^
    -e "TEXINPUTS=./out//:./:/workdir//:" ^
    -w /workdir/%DOCKER_PATH% ^
    %IMAGE_NAME% lualatex -output-directory=out -interaction=nonstopmode %FILENAME%

echo Компиляция завершена. PDF-файл должен находиться в папке %1\out.