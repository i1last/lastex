import argparse
import subprocess
import sys
import os
import time
import shutil

from core.lib.config import *
from core.lib.docker_handler import (
    ensure_container_running, 
    stop_container, 
    get_container_status, 
    copy_templates_to_tmp
)
from core.lib.path_utils import get_jobname

def run_command(project_path, target="all", tex_file=DEFAULT_FILENAME):
    start_time = time.time()
    
    # --- Валидация
    full_tex_path = os.path.join(project_path, tex_file)
    if not os.path.exists(full_tex_path):
        print(f"❌ Файл '{tex_file}' не найден в '{project_path}'")
        sys.exit(1)

    jobname = get_jobname(project_path)
    ensure_container_running()
    copy_templates_to_tmp()

    # --- Копирование глобального .latexmkrc в папку проекта
    root_dir = os.path.dirname(os.path.abspath(__file__))
    global_rc_path = os.path.join(root_dir, 'core', '.latexmkrc')

    rc_content = ""
    if os.path.exists(global_rc_path):
        with open(global_rc_path, 'r') as f:
            rc_content = f.read()
    else:
        print(f"⚠️  Глобальный конфиг {global_rc_path} не найден. Используются настройки по умолчанию.")
    
    # --- Проверяем наличие библиографии
    bib_path = os.path.join(project_path, BIB_FILE)
    has_bib = os.path.exists(bib_path)

    if not has_bib:
        # ЖЕСТКОЕ ОТКЛЮЧЕНИЕ: Если файла нет, запрещаем latexmk даже думать о bibtex
        rc_content += "\n\n# --- Auto-generated: Bibliography Disabled ---\n"
        rc_content += "$bibtex_use = 0;\n"
        print("🚫 Библиография отсутствует: Biber отключен.")
    else:
        print("📚 Библиография найдена.")

    # --- Инъекция конфига внутрь контейнера
    # Мы записываем конфиг в /root/.latexmkrc внутри Docker. 
    # Latexmk автоматически подхватывает конфиг из домашней директории пользователя.
    try:
        subprocess.run(
            ["docker", "exec", "-i", CONTAINER_NAME, "sh", "-c", "cat > /root/.latexmkrc"],
            input=rc_content.encode('utf-8'),
            check=True
        )
    except subprocess.CalledProcessError:
        print("❌ Не удалось передать конфигурацию в контейнер")
        sys.exit(1)


    print(f"📁 Проект:   {project_path}")
    print(f"📄 Файл:     {tex_file}")
    print(f"🎯 Цель:     {target}")

    # --- Формирование команды latexmk
    texfot_path = f"{TEXLIVE_BIN}/texfot"
    latexmk_path = f"{TEXLIVE_BIN}/latexmk"
    clean_path = project_path.replace('\\', '/').strip('./')

    # --- Аргументы для latexmk
    if target == "clean":
        # При очистке удаляем и папку out целиком для надежности
        out_dir = os.path.join(project_path, "out")
        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)
        latexmk_args = "-C" # Дополнительная очистка от latexmk
    else:
        latexmk_args = f"-pdflua -jobname='{jobname}'"
        print(f"🏷️  Имя выходного файла: {jobname}.pdf\n")

    # --- Команда запуска
    bash_cmd = (
        f"export PATH={TEXLIVE_BIN}:$PATH && "
        f"export TEXINPUTS={TEXINPUTS} && "
        f"cd /workdir/{clean_path} && "
        f"{texfot_path} {latexmk_path} {latexmk_args} '{tex_file}'"
    )
    
    # --- Выполнение
    result = subprocess.run(["docker", "exec", CONTAINER_NAME, "bash", "-c", bash_cmd])
    
    end_time = time.time()
    duration = end_time - start_time

    if result.returncode == 0:
        if target != "clean":
            print(f"\n✅ {jobname}.pdf создан успешно за {duration:.2f} сек.")
        else:
            print(f"\n✅ Очистка завершена.")
    else:
        print(f"\n❌ Ошибка выполнения (код: {result.returncode})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LasTeX CLI")
    parser.add_argument("command", choices=["build", "clean", "stop", "status"], help="Команда")
    parser.add_argument("path", nargs="?", help="Путь к папке проекта")
    parser.add_argument("tex_file", nargs="?", default=DEFAULT_FILENAME, help="Имя .tex файла")

    args = parser.parse_args()

    if args.command == "stop":
        stop_container()
    elif args.command == "status":
        print(get_container_status())
    elif args.command == "build":
        if not args.path: 
            print("❌ Укажите путь к проекту"); sys.exit(1)
        run_command(args.path, "all", args.tex_file)
    elif args.command == "clean":
        if not args.path: 
            print("❌ Укажите путь к проекту"); sys.exit(1)
        run_command(args.path, "clean", args.tex_file)