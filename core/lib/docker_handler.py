import subprocess
import hashlib
import os
import sys
from core.lib.config import IMAGE_NAME, CONTAINER_NAME

def get_dockerfile_hash():
    dockerfile_path = os.path.join("core", "Dockerfile")
    if not os.path.exists(dockerfile_path):
        print(f"❌ Dockerfile не найден: {dockerfile_path}")
        sys.exit(1)
    with open(dockerfile_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:12]

def get_container_status():
    res = subprocess.run(["docker", "ps", "-a", "--filter", f"name={CONTAINER_NAME}", "--format", "{{.Status}}"], 
                         capture_output=True, text=True)
    if res.stdout.startswith("Up"):
        return "🟢 Контейнер работает"
    return "🔴 Контейнер не запущен"

def stop_container():
    print("🛑 Останавливаю контейнер LaTeX...")
    subprocess.run(["docker", "stop", CONTAINER_NAME], capture_output=True)
    subprocess.run(["docker", "rm", CONTAINER_NAME], capture_output=True)
    print("✅ Контейнер остановлен")

def ensure_container_running():
    tag = f"{IMAGE_NAME}:{get_dockerfile_hash()}"
    
    # 1. Проверка образа
    if subprocess.run(["docker", "inspect", "--type=image", tag], capture_output=True).returncode != 0:
        print(f"🔨 Изменился Dockerfile. Пересборка образа: {tag}...")
        subprocess.run(["docker", "build", "-t", tag, "-t", f"{IMAGE_NAME}:latest", "-f", "core/Dockerfile", "."], check=True)
        stop_container() # Форсируем перезапуск после сборки

    # 2. Проверка работы
    status = subprocess.run(["docker", "ps", "--filter", f"name={CONTAINER_NAME}", "--format", "{{.Names}}"], 
                            capture_output=True, text=True)
    if CONTAINER_NAME not in status.stdout:
        print(f"🔧 Запуск контейнера-демона (Image: {tag})...")
        subprocess.run(["docker", "run", "-d", "--name", CONTAINER_NAME, "-v", f"{os.getcwd()}:/workdir", f"{IMAGE_NAME}:latest", "sleep", "infinity"], check=True)
    
    return CONTAINER_NAME

def copy_templates_to_tmp():
    # Эквивалент логики из Batch по копированию во временную папку
    cmd = (
        f"mkdir -p /tmp/latex-template/template && "
        f"if [ -d '/workdir/core/templates' ]; then "
        f"cp -r /workdir/core/templates/* /tmp/latex-template/template; "
        f"fi"
    )
    subprocess.run(["docker", "exec", CONTAINER_NAME, "bash", "-c", cmd], capture_output=True)