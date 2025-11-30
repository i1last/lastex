# Makefile для сборки LaTeX-документов (v3: Dynamic Jobname)

# --- Переменные ---
TEX_FILE    ?= _report.tex
# JOBNAME: имя выходного файла. Если не передано извне, берется имя TEX_FILE без расширения.
JOBNAME     ?= $(basename $(TEX_FILE))
BIB_FILE    ?= references.bib
OUT_DIR     = out

# --- Компиляторы ---
# Добавлен флаг -jobname для смены имени выходного файла
LATEX       = -lualatex -shell-escape -interaction=nonstopmode -output-directory=$(OUT_DIR) -jobname=$(JOBNAME)
BIBER       = biber

# --- Проверка, используется ли библиография ---
BIB_EXISTS  = $(shell test -f $(BIB_FILE) && echo true)

# --- Цели ---

all: pdf

# Основная цель теперь ссылается на JOBNAME
pdf: $(OUT_DIR)/$(JOBNAME).pdf

# --- Правила сборки ---

# Правило №1: Финальная сборка PDF
# ВАЖНО: Цель зависит от $(JOBNAME).pdf, но исходник — $(TEX_FILE)
ifeq ($(BIB_EXISTS),true)
$(OUT_DIR)/$(JOBNAME).pdf: $(TEX_FILE) $(OUT_DIR)/$(JOBNAME).bbl
	@echo "\n\n--- [LaTeX] Финальная компиляция (с библиографией) -> $(JOBNAME).pdf ---"
	$(LATEX) $(TEX_FILE)
else
$(OUT_DIR)/$(JOBNAME).pdf: $(TEX_FILE)
	@echo "\n\n--- [LaTeX] Финальная компиляция (без библиографии) -> $(JOBNAME).pdf ---"
	mkdir -p $(OUT_DIR)
	$(LATEX) $(TEX_FILE)
endif

# Правило №2: Создание .bbl файла
# Biber ищет .bcf файл, имя которого совпадает с JOBNAME
$(OUT_DIR)/$(JOBNAME).bbl: $(OUT_DIR)/$(JOBNAME).aux
	@echo "\n\n--- [Biber] Обработка библиографии для $(JOBNAME) ---"
	$(BIBER) $(OUT_DIR)/$(JOBNAME)
	@echo "\n\n--- [LaTeX] Промежуточная компиляция ---"
	$(LATEX) $(TEX_FILE)

# Правило №3: Создание .aux файла (первый проход)
# Цель — aux файл с именем JOBNAME, но создается он из TEX_FILE
$(OUT_DIR)/$(JOBNAME).aux: $(TEX_FILE)
	@echo "\n\n--- [LaTeX] Первый проход (создание .aux) ---"
	mkdir -p $(OUT_DIR)
	$(LATEX) $(TEX_FILE)

# Очистка
clean:
	@echo "\n\n--- Очистка временных файлов ---"
	rm -rf $(OUT_DIR)

.PHONY: all pdf clean