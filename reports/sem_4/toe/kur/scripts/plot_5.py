import numpy as np
import matplotlib.pyplot as plt
from scripts.calc_2 import tf
from scripts.calc_4 import mat
from scripts.calc_5 import ex5

t_max = ex5['t_max']
t = np.linspace(0, t_max, 500)

# Импульсная характеристика h(t)
h_t = ex5['A1'] * np.exp(tf['p1_re'] * t) + ex5['A2']['mag'] * np.exp(tf['p2_re'] * t) * np.cos(tf['p2_im'] * t + np.radians(ex5['A2']['phi']))

plt.figure()
plt.plot(t, h_t, marker='')
plt.xlabel(r'$t$, с')
plt.ylabel(r'$h(t)$')
plt.grid(True)
plt.savefig('plot_h.pgf')

# Переходная характеристика h1(t) - аналитика
h1_t = ex5['B1'] + ex5['B2'] * np.exp(tf['p1_re'] * t) + ex5['B3']['mag'] * np.exp(tf['p2_re'] * t) * np.cos(tf['p2_im'] * t + np.radians(ex5['B3']['phi']))

# Переходная характеристика h1(t) - численный расчет
dt = ex5['dt']
steps = int(t_max / dt)
t_num = np.zeros(steps + 1)
h1_num = np.zeros(steps + 1)
x = np.zeros(3)
A = np.array([[mat['A11'], mat['A12'], mat['A13']],
              [mat['A21'], mat['A22'], mat['A23']],
              [mat['A31'], mat['A32'], mat['A33']]])
B = np.array([mat['B11'], mat['B21'], mat['B31']])

for i in range(steps + 1):
    t_num[i] = i * dt
    h1_num[i] = x[2]  # Выходная переменная iL2
    x = x + dt * (A @ x + B)

plt.figure()
plt.plot(t, h1_t, label='Аналитический расчет', marker='')
plt.plot(t_num, h1_num, label='Численный расчет (Эйлер)', marker='')
plt.xlabel(r'$t$, с')
plt.ylabel(r'$h_1(t)$')
plt.legend(ncol=2)
plt.grid(True)
plt.savefig('plot_h1.pgf')