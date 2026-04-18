# --- Настройки компилятора
$pdf_mode = 4; # 4 = LuaLaTeX
$recorder = 1; # Использовать .fls файл для точного отслеживания зависимостей
$postscript_mode = $dvi_mode = 0;
$use_hash = 1;

# --- Команда компиляции
# %O - опции, передаваемые latexmk
# %S - исходный файл
# -shell-escape критичен для minted
# -synctex=1 для обратного поиска (полезно при отладке)
$lualatex = 'lualatex -file-line-error -shell-escape -interaction=nonstopmode -synctex=1 %O %S';

# --- Пользовательские зависимости
sub add_py_deps { # Отслеживает изменения в .py файлах в папке scripts/ и связывает их с основным .tex файлом.
    if (-d 'scripts') { # Проверяем, существует ли папка scripts
        my @py_files = glob "scripts/*.py"; # Находим все файлы .py в этой папке
        return @py_files; # Возвращаем их как зависимости
    }
    return ();
}
add_cus_dep('tex', 'py', 0, 'add_py_deps'); # Регистрируем нашу подпрограмму в latexmk

# --- Управление файлами
$out_dir = 'out'; # Директория для выходных файлов
$clean_ext = 'bbl nav snm vrb tr vtd tdo fls fdb_latexmk'; # Расширения файлов для очистки (команда clean)

# --- Библиография
$bibtex = 'biber %O %S'; # Устанавливаем Biber, а не BibTeX