# Makefile для сборки LaTeX-документов (умная и надежная версия v2)

# --- Переменные ---
TEX_FILE    ?= _report.tex
TARGET      = $(basename $(TEX_FILE))
BIB_FILE    ?= references.bib
OUT_DIR     = out

# --- Компиляторы ---
LATEX       = -lualatex -shell-escape -interaction=nonstopmode -output-directory=$(OUT_DIR)
BIBER       = biber

# --- Проверка, используется ли библиография ---
BIB_EXISTS  = $(shell test -f $(BIB_FILE) && echo true)

# --- Цели ---

# Цель по умолчанию: собрать PDF
all: pdf

# Основная цель: создать PDF-файл
pdf: $(OUT_DIR)/$(TARGET).pdf

# --- Правила сборки ---

# Правило №1: Финальная сборка PDF
# Зависит от .tex файла и, если нужно, от .bbl файла.
ifeq ($(BIB_EXISTS),true)
$(OUT_DIR)/$(TARGET).pdf: $(TARGET).tex $(OUT_DIR)/$(TARGET).bbl
	@echo "\n\n--- [LaTeX] Финальная компиляция (с библиографией) ---"
	$(LATEX) $(TARGET).tex
else
$(OUT_DIR)/$(TARGET).pdf: $(TARGET).tex
	@echo "\n\n--- [LaTeX] Финальная компиляция (без библиографии) ---"
	mkdir -p $(OUT_DIR)
	$(LATEX) $(TARGET).tex
endif

# Правило №2: Создание .bbl файла (библиографии)
# Зависит от .aux файла.
$(OUT_DIR)/$(TARGET).bbl: $(OUT_DIR)/$(TARGET).aux
	@echo "\n\n--- [Biber] Обработка библиографии ---"
	$(BIBER) $(OUT_DIR)/$(TARGET)
	@echo "\n\n--- [LaTeX] Повторная компиляция после Biber ---"
	$(LATEX) $(TARGET).tex

# Правило №3: Создание .aux файла (первый проход LaTeX)
# Зависит от .tex файла.
$(OUT_DIR)/$(TARGET).aux: $(TARGET).tex
	@echo "\n\n--- [LaTeX] Первый проход (создание .aux) ---"
	mkdir -p $(OUT_DIR)
	$(LATEX) $(TARGET).tex

# Цель для очистки
clean:
	@echo "\n\n--- Очистка временных файлов ---"
	rm -rf $(OUT_DIR)

# Псевдо-цели
.PHONY: all pdf clean