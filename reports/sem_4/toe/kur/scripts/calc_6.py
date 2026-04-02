from scripts.source import s
from scripts.calc_1 import n
from scripts.calc_5 import h1_t, h1_analytical

ex6 = {}
ex6['Im'] = s['Im']
ex6['tu'] = n['ti']

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

def reaction(t):
    term1 = ex6['Im'] * h1_analytical(t) if t >= 0 else 0
    term2 = ex6['Im'] * h1_analytical(t - ex6['tu']) if t >= ex6['tu'] else 0
    return term1 - term2