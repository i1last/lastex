import subprocess
import sys
import os
from core.lib.docker_handler import ensure_container_running, normalize_docker_path
from core.lib.config import DEFAULT_FILENAME, CONTAINER_NAME
from core.lib.utils import sync_matplotlib_config

def run_single_python(script_path):
    """Запускает один скрипт и перемещает результат в /pgfs/."""
    ensure_container_running()
    sync_matplotlib_config()
    
    # 1. Поиск корня проекта (где лежит _report.tex)
    script_abs = os.path.abspath(script_path)
    project_dir = os.path.dirname(script_abs)
    while project_dir != os.path.dirname(project_dir):
        if os.path.exists(os.path.join(project_dir, DEFAULT_FILENAME)):
            break
        project_dir = os.path.dirname(project_dir)
    
    # 2. Подготовка путей для Docker
    docker_project_path = normalize_docker_path(project_dir)
    rel_script_from_project = os.path.relpath(script_abs, project_dir).replace('\\', '/')
    script_base = os.path.splitext(os.path.basename(script_abs))[0]
    script_dir_rel = os.path.dirname(rel_script_from_project)

    print(f"🐍 Запуск: {rel_script_from_project} (Корень: {docker_project_path})")
    
    # 3. Команда: создать pgfs, выполнить скрипт в его папке, переместить результат
    cmd = (
        f"cd /workdir/{docker_project_path} && mkdir -p pgfs && "
        f"cd {script_dir_rel} && python3 {os.path.basename(script_abs)} && "
        f"if [ -f {script_base}.pgf ]; then mv {script_base}.pgf ../pgfs/{script_base}.pgf; fi"
    )
    
    result = subprocess.run(["docker", "exec", CONTAINER_NAME, "bash", "-c", cmd], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ График pgfs/{script_base}.pgf обновлен.")
    else:
        print(f"❌ Ошибка:\n{result.stderr}"); sys.exit(1)
    