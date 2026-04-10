import math
from scripts.source import s
from scripts.calc_1 import n
from scripts.calc_5 import h1_t, h1_analytical

ex6 = {}
ex6['Im'] = s['Im']

# Коэффициенты для функции i_21(t) = Im * h1(t)
i21_t = {
    'a': ex6['Im'] * h1_t['a'],
    'b': ex6['Im'] * h1_t['b'],
    'c': h1_t['c'],
    'd': ex6['Im'] * h1_t['d'],
    'e': h1_t['e'],
    'f': h1_t['f'],
    'g': h1_t['g']
}

# Аналитическая функция i21(t) согласно формуле (6.6)
def i21_analytical(t):
    return (
        i21_t['a'] +
        i21_t['b'] * math.exp(i21_t['c'] * t) + 
        i21_t['d'] * math.exp(i21_t['e'] * t) * math.cos(
            i21_t['f'] * t + math.radians(i21_t['g'])
        )
    )

# Реакция цепи на двуполярный меандр
def reaction(t, ti):
    term1 = i21_analytical(t) if t >= 0 else 0
    term2 = 2 * i21_analytical(t - ti) if t >= ti else 0
    term3 = i21_analytical(t - 2 * ti) if t >= 2 * ti else 0
    
    return term1 - term2 + term3
