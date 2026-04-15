import subprocess
import sys
import os
from core.lib.docker_handler import ensure_container_running, normalize_docker_path
from core.lib.config import DEFAULT_FILENAME, CONTAINER_NAME
from core.lib.utils import sync_matplotlib_config

def run_single_python(script_path):
    """Запускает один скрипт и перемещает созданные pgf/pdf в /figs/ (если они есть)."""
    ensure_container_running()
    sync_matplotlib_config()
    
    script_abs = os.path.abspath(script_path)
    project_dir = os.path.dirname(script_abs)
    # Поиск корня проекта
    while project_dir != os.path.dirname(project_dir):
        if os.path.exists(os.path.join(project_dir, DEFAULT_FILENAME)):
            break
        project_dir = os.path.dirname(project_dir)
    
    docker_project_path = normalize_docker_path(project_dir)
    rel_script_from_project = os.path.relpath(script_abs, project_dir).replace('\\', '/')
    rel_script_from_project_as_module = rel_script_from_project.replace('/', '.').replace('.py', '')

    
    # Абсолютный путь к папке pgfs внутри контейнера
    abs_figs_path = f"/workdir/{docker_project_path}/figs"

    print(f"🐍 Запуск: {rel_script_from_project} (Корень: {docker_project_path})")

    cmd = (
        f"cd /workdir/{docker_project_path} && "
        f"python3 -m {rel_script_from_project_as_module} && "
        f"files=$(find . -maxdepth 3 \\( -path './out' -o -path './figs' \\) -prune -o \\( -name '*.pdf' -o -name '*.pgf' \\) -type f -print) && "
        f"if [ -n \"$files\" ]; then "
        f"mkdir -p {abs_figs_path} && "
        f"echo \"$files\" | xargs -I {{}} mv {{}} {abs_figs_path}/; "
        f"fi"
    )
    
    # Используем Popen для живого вывода в терминал
    process = subprocess.Popen(
        ["docker", "exec", CONTAINER_NAME, "bash", "-c", cmd],
        stdout=sys.stdout, # Перенаправляем стандартный вывод в терминал
        stderr=sys.stderr, # Перенаправляем ошибки в терминал
        text=True
    )
    
    process.wait() # Ждем завершения
    
    if process.returncode == 0:
        print(f"✅ Скрипт успешно завершен.")
    else:
        print(f"❌ Ошибка выполнения скрипта (Exit code: {process.returncode})")
        sys.exit(process.returncode)