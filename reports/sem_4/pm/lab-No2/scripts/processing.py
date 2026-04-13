import math
from scripts.protocol import p, loads

# Словарь для хранения результатов расчетов
r = {
    'wood_along': {},
    'wood_across': {},
    'plastic': {}
}

# --- 1. Расчет исходных площадей поперечного сечения (в м^2) ---
# 1 см^2 = 1e-4 м^2
r['wood_along']['S0'] = p['wood_along']['before']['a'] * p['wood_along']['before']['b'] * 1e-4
r['wood_across']['S0'] = p['wood_across']['before']['a'] * p['wood_across']['before']['b'] * 1e-4
r['plastic']['S0'] = p['plastic']['before']['a'] * p['plastic']['before']['b'] * 1e-4

# --- 2. Расчет механических характеристик (в Па) ---
# 1 кН = 1e3 Н
# Формула: sigma = P / S0

# 2.1. Дерево, сжатие вдоль волокон (хрупкий материал)
# Временное сопротивление (предел прочности)
r['wood_along']['sigma_B'] = loads['P_max_wood_along'] * 1e3 / r['wood_along']['S0']
# Предел текучести отсутствует
r['wood_along']['sigma_T'] = '---'
# Напряжение в конце опыта равно пределу прочности
r['wood_along']['sigma_K'] = r['wood_along']['sigma_B']

# 2.2. Дерево, сжатие поперек волокон (пластичное поведение)
# Предел текучести (условно принимается равным пределу пропорциональности)
r['wood_across']['sigma_T'] = loads['P1_wood_across'] * 1e3 / r['wood_across']['S0']
# Временное сопротивление для материалов с площадкой текучести не определяется
r['wood_across']['sigma_B'] = '---'
# Напряжение в момент прекращения опыта
r['wood_across']['sigma_K'] = loads['Pk_wood_across'] * 1e3 / r['wood_across']['S0']

# 2.3. Пластик (пластичный материал)
# Предел текучести
r['plastic']['sigma_T'] = loads['Pt_plastic'] * 1e3 / r['plastic']['S0']
# Временное сопротивление не определяется
r['plastic']['sigma_B'] = '---'
# Напряжение в момент прекращения опыта
r['plastic']['sigma_K'] = loads['Pk_plastic'] * 1e3 / r['plastic']['S0']