import os
import re

def get_jobname(project_path):
    # Логика: отсекаем всё до sem_X включительно
    # Batch: reports\sem_3\pioa\kur -> pioa_kur
    clean_path = re.sub(r'^.*sem_\d+[\\/]', '', project_path)
    # Заменяем слэши на подчеркивания
    jobname = clean_path.replace('\\', '_').replace('/', '_').strip('_')
    return jobname if jobname else "report"