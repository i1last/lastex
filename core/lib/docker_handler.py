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
    elif res.stdout:
        return f"🟡 Контейнер существует, но не запущен ({res.stdout.strip()})"
    return "🔴 Контейнер не запущен"

def stop_container():
    print("🛑 Останавливаю контейнер LaTeX...")
    # Используем -f, чтобы не падать с ошибкой, если контейнера уже нет
    subprocess.run(["docker", "rm", "-f", CONTAINER_NAME], capture_output=True)
    print("✅ Контейнер остановлен и удален")

def ensure_container_running():
    tag = f"{IMAGE_NAME}:{get_dockerfile_hash()}"
    
    # 1. Проверка образа
    if subprocess.run(["docker", "inspect", "--type=image", tag], capture_output=True).returncode != 0:
        print(f"🔨 Изменился Dockerfile. Пересборка образа: {tag}...")
        subprocess.run(["docker", "build", "-t", tag, "-t", f"{IMAGE_NAME}:latest", "-f", "core/Dockerfile", "."], check=True)
        stop_container()

    # 2. Проверка существования (даже если он остановлен)
    # Используем 'docker ps -a', чтобы найти контейнер в любом состоянии
    check_exists = subprocess.run(["docker", "ps", "-a", "--filter", f"name={CONTAINER_NAME}", "--format", "{{.Names}}"], 
                                 capture_output=True, text=True)
    
    if CONTAINER_NAME in check_exists.stdout:
        # Проверяем, запущен ли он реально
        check_running = subprocess.run(["docker", "ps", "--filter", f"name={CONTAINER_NAME}", "--format", "{{.Names}}"], 
                                      capture_output=True, text=True)
        
        if CONTAINER_NAME not in check_running.stdout:
            print("⚠️ Контейнер найден в спящем состоянии. Перезапуск...")
            stop_container() # Удаляем старый "труп" перед новым запуском
        else:
            return CONTAINER_NAME # Всё ок, уже работает

    # 3. Запуск
    print(f"🔧 Запуск контейнера-демона (Image: {tag})...")
    try:
        subprocess.run([
            "docker", "run", "-d", 
            "--name", CONTAINER_NAME, 
            "-v", f"{os.getcwd()}:/workdir", 
            f"{IMAGE_NAME}:latest", 
            "sleep", "infinity"
        ], check=True)
    except subprocess.CalledProcessError:
        print("❌ Критическая ошибка при запуске Docker. Попробуйте выполнить 'docker rm -f latex-daemon' вручную.")
        sys.exit(1)
    
    return CONTAINER_NAME

def copy_templates_to_tmp():
    cmd = (
        f"mkdir -p /tmp/latex-template/template && "
        f"if [ -d '/workdir/core/templates' ]; then "
        f"cp -r /workdir/core/templates/* /tmp/latex-template/template; "
        f"fi"
    )
    subprocess.run(["docker", "exec", CONTAINER_NAME, "bash", "-c", cmd], capture_output=True)

def normalize_docker_path(local_path):
    """Преобразует локальный путь в путь внутри контейнера (/workdir/...)."""
    # Получаем путь относительно корня проекта (где лежит lastex.py)
    root_dir = os.path.dirname(os.path.abspath(__file__))
    abs_path = os.path.abspath(local_path)
    
    try:
        rel_path = os.path.relpath(abs_path, root_dir)
    except ValueError:
        print(f"❌ Ошибка: Путь {local_path} находится вне папки проекта.")
        sys.exit(1)

    # Заменяем обратные слеши на прямые для Linux/Docker
    clean_path = rel_path.replace('\\', '/').strip('./')
    return clean_path
