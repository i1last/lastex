IMAGE_NAME = "latex-compiler-env"
CONTAINER_NAME = "latex-daemon"
DEFAULT_FILENAME = "_report.tex"
BIB_FILE = "references.bib"
TEXLIVE_BIN = "/usr/local/texlive/2025/bin/x86_64-linux"

# Пути ВНУТРИ контейнера (всегда Linux-style)
WORKDIR = "/workdir"
TEMP_TEMPLATE_PATH = "/tmp/latex-template/template"
CORE_MAKEFILE = "/workdir/core/Makefile"

# Настройка TEXINPUTS
TEXINPUTS = f".:{TEMP_TEMPLATE_PATH}//::"