from scripts.protocol import p

r = {}

# Задание 1: Напряжение смещения, приведенное ко входу
r['U_cm_in'] = -p['v']['Uout'] * (p['r']['R1'] / p['r']['R12'])

# Задание 2: Передаточная характеристика (диапазон -1.2 .. 1.2 В)
idx_lin = [i for i, u in enumerate(p['tc']['Uin']) if -1.2 <= u <= 1.2]
u_in_lin =[p['tc']['Uin'][i] for i in idx_lin]
u_out14_lin = [p['tc']['UforR14'][i] for i in idx_lin]
u_out15_lin = [p['tc']['UforR15'][i] for i in idx_lin]

# Расчет коэффициента передачи по крайним точкам выбранного диапазона
r['U_in_min'] = u_in_lin[0]
r['U_in_max'] = u_in_lin[-1]
r['dU_in'] = r['U_in_max'] - r['U_in_min']

r['U_out14_min'] = u_out14_lin[0]
r['U_out14_max'] = u_out14_lin[-1]
r['dU_out14'] = r['U_out14_max'] - r['U_out14_min']
r['K_14'] = r['dU_out14'] / r['dU_in']

r['U_out15_min'] = u_out15_lin[0]
r['U_out15_max'] = u_out15_lin[-1]
r['dU_out15'] = r['U_out15_max'] - r['U_out15_min']
r['K_15'] = r['dU_out15'] / r['dU_in']

# Задание 3: АЧХ
# Расчет модуля коэффициента усиления K = U_out / U_in
r['K_afc'] = [u / p['afcd']['Uin'] for u in p['afcd']['Uout']]

# Задание 4: Скорость нарастания
# Данные считаны с осциллограммы
r['div_y'] = 2.6        # Количество делений по вертикали (размах)
r['scale_y'] = 5.0      # Масштаб по вертикали, В/дел
r['Delta_U'] = r['div_y'] * r['scale_y']

r['div_x'] = 1          # Количество делений по горизонтали (фронт)
r['scale_x'] = 2e-6     # Масштаб по горизонтали, с/дел
r['tau_fr'] = r['div_x'] * r['scale_x']

r['v_slew'] = r['Delta_U'] / r['tau_fr']
r['v_slew_V_us'] = r['v_slew'] / 1e6