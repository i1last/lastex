# Подготовка перед использованием
## Хранение pdf файлов
Рекомендуется настроить Git LFS (cм. [статью об ограничениях](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage)) для хранения pdf файлов. В случае, если пользователя это не устраивает, он может расскоментировать соотв. строку в файле `.gitignore`.

**Инструкция по настройке Git LFS:**
1.  **Установить Git LFS.** Это делается один раз на вашем компьютере. Инструкции есть на официальном сайте [git-lfs.github.com](https://git-lfs.github.com/).
2.  **Инициализировать LFS в репозитории.** В корневой папке проекта выполните команду:
    ```bash
    git lfs install
    ```
3.  **Указать Git отслеживать PDF-файлы через LFS.** Эта команда добавит правило в новый файл `.gitattributes`:
    ```bash
    git lfs track "*.pdf"
    ```
4.  **Добавить `.gitattributes` в репозиторий.**
    ```bash
    git add .gitattributes
    ```

## Шрифт Times New Roman
1. Найдите шрифты на вашем компьютере. Откройте Проводник и перейдите в папку `C:\Windows\Fonts`.
2. Скопируйте необходимые файлы. Найдите и скопируйте следующие четыре файла:
   - `times.ttf` (Обычный - Times New Roman)
   - `timesbd.ttf` (Полужирный - Times New Roman Bold)
   - `timesbi.ttf` (Полужирный курсив - Times New Roman Bold Italic)
   - `timesi.ttf` (Курсив - Times New Roman Italic)
3. Вставьте скопированные четыре `.ttf` файла в эту новую папку `fonts/`. Важно, чтобы имена соответствовали тем, что перечислены в п. 2 (регистр имеет значение).

# Использование в VS Code
## Конфигурация окружения
1. Откройте "Open Keyboard Shortcuts (JSON)" в палитре команд (Ctrl + Shift + P).
2. В открывшийся файл `keybindings.json` добавьте следующий объект внутрь существующих квадратных скобок []. Если файл пуст, просто вставьте весь блок.
```JSON
{
    "key": "ctrl+alt+b",
    "command": "workbench.action.tasks.runTask",
    "args": "Compile Current LaTeX Report"
}
```
Открыв `_report.tex` и нажав Ctrl + Alt + B запустится процесс компиляции.

## Сниппеты
Проект уже включает набор готовых сниппетов для ускорения работы, которые хранятся в файле `.vscode/latex.code-snippets`. Они станут доступны автоматически после открытия папки проекта в VS Code.

# Работа с проектом
## Создание нового отчёта
1.  **Скопируйте шаблон.** Перейдите в папку `template/`, скопируйте файл `_report.tex` (имя файла должно строго быть именно таким).
2.  **Вставьте шаблон в папку с работой.** Создайте новую папку для вашей работы в соответствующей директории (например, `reports/year_1/semester_1/physics/lab_01/`) и вставьте туда скопированный файл.
3.  **Заполните данные.** Откройте `_report.tex` и отредактируйте поля в секции "КОНФИГУРАЦИЯ ДАННЫХ ДЛЯ ТИТУЛЬНОГО ЛИСТА" (название работы, дисциплина, ФИО и т.д.).
4.  **Пишите отчет.** Содержание отчета рекомендуется делать в отличном от `_report.tex` файле, т.к. он является сервисным. Вы можете писать отчет, например, в файле `main.tex` или в файлах `char1.tex`, `char2.tex` и т.д. Главное правильно импортируйте их в файле `_report.tex`.
5.  **Скомпилируйте.** Запустите скрипт компиляции из корневой папки проекта:
    ```bash
    .\compile.bat reports/year_1/semester_1/physics/lab_01
    ```
    Для подробной инструкции использования `compile.bat` введите `.\compile.bat` в терминале.

# Полезные ссылки
- https://open-resource.ru/spisok-literatury/
- https://samolisov.blogspot.com/2008/06/latex_09.html

# Latex Workshop
Используйте Latex Workshop для подсказок в коде.
`latex-workshop.latex.autoBuild.run` лучше поставить `never`, т.к. в данном проекте своя команда для сборки.

## Форматирование
Для форматирования скачайте `latexindent.exe` с соотв. [github репозитория](https://github.com/cmhughes/latexindent.pl) и поместите в какую-нибудь папку на вашем диске. Далее для настройки `latex-workshop.formatting.latexindent.path` указываем путь к .exe файлу (напр, `C:\path\to\latexindent.exe`). Не забываем установить `latex-workshop.formatting.latex` на `latexindent`.

## Линтинг
Я еще не разобрался, как это должно работать.
Аналогично форматированию. Я использую [LaCheck](https://github.com/mitchmoser/LACheck). `latex-workshop.linting.lacheck.enabled` = `true`, `latex-workshop.linting.lacheck.exec.path` = `C:\path\to\LACheck.exe`.

---

[ГОСТ 7.32-2017](https://cs.msu.ru/sites/cmc/files/docs/2021-11gost_7.32-2017.pdf), в соотв. с которым разрабатывается проект.