import argparse
import subprocess
import sys
import os
import time

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
    
    # Валидация
    full_tex_path = os.path.join(project_path, tex_file)
    if not os.path.exists(full_tex_path):
        print(f"❌ Файл '{tex_file}' не найден в '{project_path}'")
        sys.exit(1)

    jobname = get_jobname(project_path)
    ensure_container_running()
    copy_templates_to_tmp()

    print(f"📁 Проект:  {project_path}")
    print(f"📄 Файл:    {tex_file}")
    print(f"🎯 Цель:   {target}")
    print(f"🏷️  Имя выходного файла: {jobname}.pdf\n")

    # Формирование bash команды с полными путями
    texfot_path = f"{TEXLIVE_BIN}/texfot"
    clean_path = project_path.replace('\\', '/').strip('./')
    bash_cmd = (
        f"export PATH={TEXLIVE_BIN}:$PATH && "
        f"export TEXINPUTS={TEXINPUTS} && "
        f"cd /workdir/{clean_path} && "
        f"{texfot_path} make -f {CORE_MAKEFILE} {target} "
        f"TEX_FILE='{tex_file}' BIB_FILE='{BIB_FILE}' JOBNAME='{jobname}'"
    )

    result = subprocess.run(["docker", "exec", CONTAINER_NAME, "bash", "-c", bash_cmd])
    
    end_time = time.time()
    duration = end_time - start_time

    if result.returncode == 0:
        print(f"\n✅ {jobname}.pdf создан успешно за {duration:.2f} сек.")
    else:
        print(f"\n❌ Ошибка компиляции (код: {result.returncode})")

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