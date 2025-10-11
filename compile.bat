@echo off
REM Скрипт для компиляции LaTeX-проекта с помощью Docker.
REM Использование: .\compile.bat reports\имя_папки_с_работой

REM Проверка, был ли передан аргумент
IF "%1"=="" (
    echo Ошибка: Укажите путь к папке с работой.
    echo Пример: .\compile.bat reports\lab_01_example
    exit /b 1
)

REM Имя для нашего Docker-образа
set IMAGE_NAME=latex-compiler-env

REM Проверяем, существует ли образ, и если нет - собираем его
docker inspect --type=image %IMAGE_NAME% > nul 2> nul
IF errorlevel 1 (
    echo Образ %IMAGE_NAME% не найден. Начинаю сборку...
    docker build -t %IMAGE_NAME% .
)

echo Запускаю компиляцию в папке: %1

REM Запускаем контейнер Docker
docker run --rm -v "%cd%":/workdir -w /workdir/%1 lualatex main.tex

echo Компиляция завершена. PDF-файл находится в папке %1.