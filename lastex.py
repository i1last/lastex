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

    # --- 4. Сборка LaTeX ---
    clean_project_path = normalize_docker_path(project_path)

    print(f"📁 Проект:   {project_path}")
    print(f"📄 Файл:     {tex_file}")
    
    texfot_path = f"{TEXLIVE_BIN}/texfot"
    latexmk_path = f"{TEXLIVE_BIN}/latexmk"

    if target == "clean":
        out_dir = os.path.join(project_path, "out")
        figs_dir = os.path.join(project_path, "figs")
        
        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)
        
        # Удаляем папку pgfs при очистке
        if os.path.exists(figs_dir):
            shutil.rmtree(figs_dir)
             
        latexmk_args = "-C"
        print("🧹 Очистка временных файлов и графиков...")
    else:
        latexmk_args = f"-pdflua -jobname='{jobname}'"
        print(f"🏷️  Имя выходного файла: {jobname}.pdf")

    bash_cmd = (
        f"export PATH={TEXLIVE_BIN}:$PATH && "
        f"export TEXINPUTS={TEXINPUTS} && "
        f"cd /workdir/{clean_project_path} && "
        f"{texfot_path} {latexmk_path} {latexmk_args} '{tex_file}'"
    )
    
    result = subprocess.run(["docker", "exec", CONTAINER_NAME, "bash", "-c", bash_cmd])
    
    duration = time.time() - start_time
    
    if target != "clean":
        print(f"\n✅ Компиляция завершена. Время: {duration:.2f} сек. См. результаты выше. Код ошибки: {result.returncode}")
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