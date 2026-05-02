# scripts/calc.py
from scripts.protocol import *

r = {}

# Номинальные параметры элементов цепи
r['R1'] = 1500
r['R2'] = 1500
r['R3'] = 3000
r['R4'] = 3000
r['U_nom'] = 2.0
r['I_nom'] = 1.0e-3

# 1. Проверка законов Кирхгофа
r['KCL_A'] = - p['ef']['I1'] - p['ef']['I2'] + p['ef']['I3']
r['KCL_D'] = p['ef']['I2'] + p['ef']['I4'] - p['ef']['I']
r['KVL_1'] = p['ef']['U1'] + p['ef']['U3'] - p['ef']['U']
r['KVL_2_sum'] = -p['ef']['U2'] + p['ef']['U4'] - p['ef']['U3']

# 2. Метод наложения (расчет токов по частичным)
r['I1_sup'] = p['s']['onlyU']['I1'] - p['s']['onlyI']['I1']
r['I2_sup'] = p['s']['onlyI']['I2'] - p['s']['onlyU']['I2']
r['I3_sup'] = p['s']['onlyU']['I3'] + p['s']['onlyI']['I3']
r['I4_sup'] = p['s']['onlyU']['I4'] + p['s']['onlyI']['I4']

# Массивы для таблицы сравнения
r['sup_branches'] =[1, 2, 3, 4]
r['sup_meas'] = [p['ef']['I1'], p['ef']['I2'], p['ef']['I3'], p['ef']['I4']]
r['sup_calc'] = [r['I1_sup'], r['I2_sup'], r['I3_sup'], r['I4_sup']]

# 3. Метод эквивалентного источника (теоретический расчет)
r['Re'] = r['R1'] + (r['R3'] * (r['R2'] + r['R4'])) / (r['R3'] + r['R2'] + r['R4'])

# Расчет U0 методом узловых потенциалов (ветвь 3 отключена)
G_A = 1/r['R1'] + 1/r['R2']
G_D = 1/r['R2'] + 1/r['R4']
G_AD = 1/r['R2']
J_A = r['U_nom'] / r['R1']
J_D = r['I_nom']

det = G_A * G_D - G_AD**2
V_A = (J_A * G_D + J_D * G_AD) / det
r['U0_th'] = V_A
r['I3_th'] = r['U0_th'] / r['Re']

# 4. Расчеты для ответов на вопросы
r['U_CD'] = p['ef']['U1'] - p['ef']['U2']
r['U_new'] = r['U_nom'] * (p['s']['onlyI']['I1'] / p['s']['onlyU']['I1'])
r['I1_Q6'] = p['s']['onlyU']['I4']