# --- Настройки компилятора ---
$pdf_mode = 4; # 4 = LuaLaTeX
$postscript_mode = $dvi_mode = 0;

# Команда компиляции. 
# %O - опции, передаваемые latexmk
# %S - исходный файл
# -shell-escape критичен для minted
# -synctex=1 для обратного поиска (полезно при отладке)
$lualatex = 'lualatex -shell-escape -interaction=nonstopmode -synctex=1 %O %S';

# --- Управление файлами ---
$out_dir = 'out'; # Директория для выходных файлов

# Расширения файлов для очистки (команда clean)
$clean_ext = 'bbl nav snm vrb tr vtd tdo fls fdb_latexmk';

# --- Библиография ---
# 1.5 = Автоматическое определение (Biber или BibTeX)
$bibtex_use = 1.5;