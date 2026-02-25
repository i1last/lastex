import argparse
import subprocess
import sys
import os
import time
import shutil

# Импорт конфигураций и библиотек
from core.lib.config import *
from core.lib.docker_handler import (
    ensure_container_running, 
    stop_container, 
    get_container_status, 
    copy_templates_to_tmp,
    normalize_docker_path
)
from core.lib.python_handler import run_single_python
from core.lib.utils import get_jobname
from core.lib.utils import sync_matplotlib_config


def build_project(project_path, tex_file=DEFAULT_FILENAME, target="all"):
    start_time = time.time()
    
    # --- 1. Валидация путей ---
    full_tex_path = os.path.join(project_path, tex_file)
    if not os.path.exists(full_tex_path):
        print(f"❌ Файл точки входа '{tex_file}' не найден в '{project_path}'")
        sys.exit(1)

    jobname = get_jobname(project_path)
    ensure_container_running()
    sync_matplotlib_config()
    copy_templates_to_tmp()

    # --- 2. Настройка Latexmk ---
    root_dir = os.path.dirname(os.path.abspath(__file__))
    global_rc_path = os.path.join(root_dir, 'core', '.latexmkrc')
    
    rc_content = ""
    if os.path.exists(global_rc_path):
        with open(global_rc_path, 'r') as f:
            rc_content = f.read()
    else:
        print(f"⚠️  Глобальный конфиг {global_rc_path} не найден.")

    bib_path = os.path.join(project_path, BIB_FILE)
    if not os.path.exists(bib_path):
        rc_content += "\n$bibtex_use = 0;\n"
        print("🚫 Библиография отсутствует: Biber отключен.")
    else:
        print("📚 Библиография найдена.")

    try:
        subprocess.run(
            ["docker", "exec", "-i", CONTAINER_NAME, "sh", "-c", "cat > /root/.latexmkrc"],
            input=rc_content.encode('utf-8'),
            check=True
        )
    except subprocess.CalledProcessError:
        print("❌ Ошибка передачи конфигурации в контейнер")
        sys.exit(1)

    # --- 3. Генерация графиков (Python) ---
    clean_project_path = normalize_docker_path(project_path)

    if target != "clean":
        print(f"📊 Обновление графиков в: {project_path}")
        
        # Абсолютный путь к папке pgfs внутри контейнера
        abs_pgfs_path = f"/workdir/{clean_project_path}/pgfs"
        
        # Сложная команда bash для xargs.
        # 1. Находим все .py файлы.
        # 2. xargs запускает bash для каждого файла параллельно.
        # 3. Внутри bash: переход в папку, запуск, проверка наличия .pgf, перемещение.
        # Используем `ls *.pgf >/dev/null 2>&1` для проверки существования файлов без вывода ошибок.
        
        py_cmd = (
            f"cd /workdir/{clean_project_path} && "
            f"find . -maxdepth 2 -name '*.py' -print0 | "
            f"xargs -0 -n1 -P$(nproc) -I {{}} bash -c '"
            f"  script=\"{{}}\"; "
            f"  dir=$(dirname \"$script\"); "
            f"  base=$(basename \"$script\" .py); "
            f"  echo \"   Running $script...\"; "
            f"  (cd \"$dir\" && python3 \"$base.py\"); "
            f"  ret=$?; "
            f"  if [ $ret -ne 0 ]; then echo \"❌ Error in $script\"; exit $ret; fi; "
            f"  count=`ls \"$dir\"/*.pgf 2>/dev/null | wc -l`; "
            f"  if [ $count -gt 0 ]; then "
            f"      mkdir -p \"{abs_pgfs_path}\"; "
            f"      mv \"$dir\"/*.pgf \"{abs_pgfs_path}/\"; "
            f"  fi"
            f"'"
        )
        
        # capture_output=False, чтобы видеть вывод параллельных процессов в реальном времени (или True, если нужен чистый лог)
        # Здесь лучше capture_output=True, чтобы не смешивать потоки вывода, а потом вывести stderr если есть ошибки.
        py_result = subprocess.run(["docker", "exec", CONTAINER_NAME, "bash", "-c", py_cmd], capture_output=True, text=True)
        
        if py_result.returncode != 0:
            print(f"❌ Ошибка при генерации графиков:\n{py_result.stderr}")
            # Не выходим, если ошибка не критична? Нет, лучше выйти, если графики сломались.
            sys.exit(1)
        elif py_result.stderr and "Traceback" in py_result.stderr:
             # Иногда python пишет в stderr даже предупреждения, но если там Traceback - это проблема.
             print(f"⚠️  Warnings/Errors:\n{py_result.stderr}")

    # --- 3.5. Генерация формата (Precompiled Preamble) ---
    fmt_jobname = "etulab_fmt"
    out_dir = "out"
    fmt_file_path = os.path.join(project_path, out_dir, f"{fmt_jobname}.fmt")
    
    # Путь к локальному файлу класса для проверки обновлений
    root_dir = os.path.dirname(os.path.abspath(__file__))
    cls_file_path = os.path.join(root_dir, "core", "templates", "etulab.cls")
    
    # 1. Проверка необходимости сборки формата
    need_fmt_build = True
    if os.path.exists(fmt_file_path):
        if os.path.exists(cls_file_path):
            fmt_time = os.path.getmtime(fmt_file_path)
            cls_time = os.path.getmtime(cls_file_path)
            if fmt_time > cls_time:
                need_fmt_build = False
        else:
            need_fmt_build = False # Если локальный класс не найден, используем существующий .fmt

    current_texinputs = f".:{out_dir}//:{TEMP_TEMPLATE_PATH}//::"

    # 2. Условная генерация
    if need_fmt_build:
        print("⚡ Генерация нативного формата (кэш устарел или отсутствует)...")
        
        fmt_source = "fmt_builder.tex"
        with open(os.path.join(project_path, fmt_source), "w") as f:
            f.write("\\documentclass{etulab}\n\\dump\n")

        if os.path.exists(fmt_file_path):
            os.remove(fmt_file_path)

        fmt_cmd = (
            f"export TEXINPUTS={current_texinputs} && "
            f"cd /workdir/{clean_project_path} && "
            f"mkdir -p {out_dir} && "
            f"lualatex -ini -interaction=nonstopmode "
            f"-output-directory={out_dir} "
            f"-jobname='{fmt_jobname}' "
            f"'&lualatex' {fmt_source}"
        )
        
        fmt_result = subprocess.run(
            ["docker", "exec", CONTAINER_NAME, "bash", "-c", fmt_cmd],
            capture_output=True, text=True
        )
        
        try:
            os.remove(os.path.join(project_path, fmt_source))
        except OSError:
            pass

        if os.path.exists(fmt_file_path):
            print("✅ Формат успешно создан.")
        else:
            print(f"❌ Критическая ошибка генерации формата: {fmt_result.stderr}")
    else:
        print("⏩ Использование закэшированного формата (etulab_fmt.fmt).")

    # --- 4. Сборка LaTeX ---
    print(f"📁 Проект:   {project_path}")
    print(f"📄 Файл:     {tex_file}")
    
    texfot_path = f"{TEXLIVE_BIN}/texfot"
    latexmk_path = f"{TEXLIVE_BIN}/latexmk"

    if target == "clean":
        out_dir = os.path.join(project_path, "out")
        pgfs_dir = os.path.join(project_path, "pgfs")
        
        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)
        
        # Удаляем папку pgfs при очистке
        if os.path.exists(pgfs_dir):
             shutil.rmtree(pgfs_dir)
             
        latexmk_args = "-C"
        print("🧹 Очистка временных файлов и графиков...")
    else:
        latexmk_args = f"-pdflua -jobname='{jobname}'"
        print(f"🏷️  Имя выходного файла: {jobname}.pdf")

    bash_cmd = (
        f"export PATH={TEXLIVE_BIN}:$PATH && "
        f"export TEXINPUTS={TEXINPUTS} && "
        f"cd /workdir/{clean_project_path} && "
        f"mkdir -p pgfs/cache && "
        f"{texfot_path} {latexmk_path} {latexmk_args} '{tex_file}'"
    )
    
    result = subprocess.run(["docker", "exec", CONTAINER_NAME, "bash", "-c", bash_cmd])
    
    duration = time.time() - start_time
    
    if target != "clean":
        print(f"\n✅ Успешно! Время: {duration:.2f} сек. Код ошибки: {result.returncode}")
    else:
        print(f"\n✅ Очистка завершена.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LasTeX CLI")
    parser.add_argument("command", choices=["build", "clean", "stop", "status"], help="Команда")
    parser.add_argument("path", nargs="?", help="Путь к файлу (.tex, .py) или папке")

    args = parser.parse_args()

    if args.command == "stop":
        stop_container()
        sys.exit(0)
    elif args.command == "status":
        print(get_container_status())
        sys.exit(0)

    if not args.path:
        print("❌ Ошибка: Не указан путь к файлу или проекту.")
        sys.exit(1)

    abs_path = os.path.abspath(args.path)
    if not os.path.exists(abs_path):
        print(f"❌ Путь не найден: {args.path}")
        sys.exit(1)

    if os.path.isfile(abs_path):
        filename = os.path.basename(abs_path)
        ext = os.path.splitext(filename)[1].lower()
        
        if ext == '.py' and args.command == "build":
            run_single_python(abs_path)
        elif ext == '.tex':
            project_dir = os.path.dirname(abs_path)
            while project_dir != os.path.dirname(project_dir):
                if os.path.exists(os.path.join(project_dir, DEFAULT_FILENAME)):
                    break
                project_dir = os.path.dirname(project_dir)
            build_project(project_dir, tex_file=DEFAULT_FILENAME, target=args.command)
        else:
            sys.exit(1)
            
    elif os.path.isdir(abs_path):
        build_project(abs_path, tex_file=DEFAULT_FILENAME, target=args.command)