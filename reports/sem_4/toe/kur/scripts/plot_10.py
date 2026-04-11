import numpy as np
import matplotlib.pyplot as plt
from scripts.calc_10 import ex10

# --- Графики дискретных спектров ---
k = np.array(ex10['k'])
A1k = np.array(ex10['A1k'])
Phi1k_deg = np.array(ex10['Phi1k_deg'])

# Амплитудный дискретный спектр
plt.figure()
plt.stem(k, A1k, linefmt='k--', markerfmt='ko', basefmt='k-')
plt.xlabel(r'$k$')
plt.ylabel(r'$A_{1k}$')
plt.xticks(k)
plt.savefig('plot_disc_spec_A.pgf')
plt.close()

# Фазовый дискретный спектр
plt.figure()
plt.stem(k, Phi1k_deg, linefmt='k--', markerfmt='ko', basefmt='k-')
plt.xlabel(r'$k$')
plt.ylabel(r'$\Phi_{1k}, ^\circ$')
plt.xticks(k)
plt.ylim(-10, 10) # Улучшение вида для нулевой фазы
plt.savefig('plot_disc_spec_Phi.pgf')
plt.close()

# --- График аппроксимации ряда Фурье ---
T = ex10['T']
t = np.linspace(-0.5 * T, 1.5 * T, 1000)

# Исходный меандр
y_input = np.piecewise(t,
    [
        (t % T < T / 2)
    ], 
    [
        ex10['A1k'][1] * np.pi / 4, # Im
        -ex10['A1k'][1] * np.pi / 4 # -Im
    ]
)

# Аппроксимация
y_approx = np.full_like(t, ex10['A1_0'])
harmonics_lines = []
for i, k_val in enumerate(ex10['k']):
    if k_val != 0:
        harmonic = ex10['A1k'][i] * np.cos(k_val * ex10['w1'] * t + np.radians(ex10['Phi1k_deg'][i]))
        y_approx += harmonic
        harmonics_lines.append(harmonic)

plt.figure()
plt.plot(t, y_input, '--', label='Исходный сигнал', color='black')
plt.plot(t, y_approx, '-', label='Аппроксимация рядом Фурье', color='red')

# Добавление отдельных гармоник тонкими линиями
colors = ['blue', 'green', 'purple']
for i, h_line in enumerate(harmonics_lines):
    if i < len(colors):
        plt.plot(t, h_line, ':', linewidth=1, color=colors[i], label=f'Гармоника k={ex10["k"][i+1]}')

plt.xlabel(r'$t$')
plt.ylabel(r'$i_1(t)$')
plt.legend()
plt.savefig('plot_fourier_approx.pgf')
plt.close()