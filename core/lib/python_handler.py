import subprocess
import sys
import os
from core.lib.docker_handler import ensure_container_running, normalize_docker_path
from core.lib.config import DEFAULT_FILENAME, CONTAINER_NAME
from core.lib.utils import sync_matplotlib_config

def run_single_python(script_path):
    """Запускает один скрипт и перемещает ВСЕ созданные pgf в /pgfs/."""
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
    script_dir_rel = os.path.dirname(rel_script_from_project)
    
    # Абсолютный путь к папке pgfs внутри контейнера
    abs_figs_path = f"/workdir/{docker_project_path}/figs"

    print(f"🐍 Запуск: {rel_script_from_project} (Корень: {docker_project_path})")
    
    # Команда обновлена:
    # 1. Переходим в папку скрипта.
    # 2. Запускаем скрипт.
    # 3. Проверяем наличие *.pgf.
    # 4. Если есть -> mkdir pgfs -> mv *.pgf
    cmd = (
        f"cd /workdir/{docker_project_path}/{script_dir_rel} && "
        f"python3 {os.path.basename(script_abs)} && "
        f"count=`ls *.pgf 2>/dev/null | wc -l`; "
        f"if [ $count -gt 0 ]; then "
        f"    mkdir -p {abs_figs_path}; "
        f"    mv *.pgf {abs_figs_path}/; "
        f"fi"
    )
    
    result = subprocess.run(["docker", "exec", CONTAINER_NAME, "bash", "-c", cmd], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Скрипт выполнен.")
        if result.stderr:
             # Выводим stderr (предупреждения matplotlib и т.д.)
             print(f"📄 Log:\n{result.stderr}")
    else:
        print(f"❌ Ошибка выполнения скрипта:\n{result.stderr}")
        sys.exit(1)