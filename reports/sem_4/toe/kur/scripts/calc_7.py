import numpy as np
from scipy.optimize import fsolve
from scripts.calc_6 import ex6
from scripts.calc_3 import freq

ex7 = {}

# Перенос базовых параметров
Im = ex6['Im']
tu = ex6['tu']

# Значение амплитудного спектра на нулевой частоте (площадь импульса)
ex7['A1_0'] = Im * tu

# Частота первого нуля спектра
ex7['w_y1'] = 2 * np.pi / tu

# Функция амплитудного спектра для численного поиска
def A1_func(w):
    if w == 0:
        return ex7['A1_0']
    return np.abs((2 * Im / w) * np.sin(w * tu / 2))

# Определение ширины спектра по 10%-му критерию
target_level = 0.1 * ex7['A1_0']

# Начальное приближение (из свойства функции sinc(x) = 0.1 при x ~ 2.85)
guess = 5.7 / tu 

def eq(w):
    return A1_func(w) - target_level

w_sp = fsolve(eq, guess)[0]
ex7['w_sp'] = w_sp

# Полоса пропускания цепи (из п. 3)
ex7['w_c'] = freq['w_c']