import numpy as np
import matplotlib.pyplot as plt
from scripts.calc_2 import tf
from scripts.calc_4 import mat
from scripts.calc_5 import res

t_max = res['t_max']
t = np.linspace(0, t_max, 500)

# Импульсная характеристика h(t)
h_t = res['A1_r'] * np.exp(tf['p1_re'] * t) + res['A2_mag'] * np.exp(tf['p2_re'] * t) * np.cos(tf['p2_im'] * t + np.radians(res['A2_arg']))

plt.figure()
plt.plot(t, h_t, color='blue')
plt.xlabel(r'$t$, с')
plt.ylabel(r'$h(t)$')
plt.grid(True)
plt.savefig('plot_h.pgf')

# Переходная характеристика h1(t) - аналитика
h1_t = res['B0'] + res['B1_r'] * np.exp(tf['p1_re'] * t) + res['B2_mag'] * np.exp(tf['p2_re'] * t) * np.cos(tf['p2_im'] * t + np.radians(res['B2_arg']))

# Переходная характеристика h1(t) - численный расчет
dt = res['dt']
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
plt.plot(t, h1_t, label='Аналитический расчет', color='blue')
plt.plot(t_num, h1_num, '--', label='Численный расчет (Эйлер)', color='red')
plt.xlabel(r'$t$, с')
plt.ylabel(r'$h_1(t)$')
plt.legend()
plt.grid(True)
plt.savefig('plot_h1.pgf')