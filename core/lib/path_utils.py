import re

def get_jobname(project_path):
    """
    Генерирует имя выходного файла с сохранением номера семестра.
    Пример: reports/sem_3/pioa/kur -> sem_3__pioa__kur
    """
    # 1. Нормализуем слэши (приводим к Linux-style)
    path = project_path.replace('\\', '/')
    
    # 2. Ищем вхождение 'sem_' и захватываем всё, начиная с него
    # Регулярное выражение ищет 'sem_', за которым идут цифры, и забирает остаток строки
    match = re.search(r'(sem_\d+.*)', path)
    
    if match:
        clean_path = match.group(1)
    else:
        # Если структура нарушена, берем базовое имя последней папки
        clean_path = path.strip('/').split('/')[-1]
    
    # 3. Формируем jobname:
    # - убираем слеши по краям
    # - заменяем внутренние слеши на двойное подчеркивание
    jobname = clean_path.strip('/').replace('/', '__')
    
    return jobname if jobname else "report"