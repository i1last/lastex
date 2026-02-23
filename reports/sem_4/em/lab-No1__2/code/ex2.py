import matplotlib.pyplot as plt
import numpy as np

# Геометрические параметры (S в м^2, l в м)
# k = S / l
k_si = (0.2 * 1e-6) / 0.03
k_ge = (0.2 * 1e-6) / 0.03
k_sic = (1.2 * 1e-6) / 0.01  # Исправленный коэффициент
k_insb = (0.1 * 1e-6) / 0.02

# Температурные точки (Кельвины)
# Общий ряд для Si, Ge, SiC
T_common = np.array([298, 308, 318, 328, 338, 348, 358, 368, 378, 388, 400])
# Ряд для InSb (нет измерения при 308 К)
T_insb   = np.array([298,      318, 328, 338, 348, 358, 368, 378, 388, 400])

# Экспериментальные данные сопротивления R (Ом)
R_si   = np.array([110.7, 114.4, 117.5, 120.7, 123.8, 127.9, 131.0, 134.3, 138.1, 141.8, 145.0])
R_ge   = np.array([292, 303, 319, 326, 339, 328, 324, 312, 285, 262.2, 211])
R_sic  = np.array([4874, 4556, 4205, 3722, 3090, 2600, 2225, 1965, 1658, 1462, 1142])
R_insb = np.array([59.2, 53.8, 50.7, 47.8, 44.3, 38.0, 35.5, 33.8, 34.9, 33.8])

def process_data(T, R, k):
    """
    Расчет координат для графика Аррениуса.
    X = 1000 / T
    Y = ln(gamma) = ln(1 / (R * k))
    """
    rho = R * k
    gamma = 1 / rho
    x_vals = 1000 / T
    y_vals = np.log(gamma)
    return x_vals, y_vals

# Обработка данных
x_si, y_si = process_data(T_common, R_si, k_si)
x_ge, y_ge = process_data(T_common, R_ge, k_ge)
x_sic, y_sic = process_data(T_common, R_sic, k_sic)
x_insb, y_insb = process_data(T_insb, R_insb, k_insb)

# Построение графика
plt.figure()

# Отрисовка кривых
plt.plot(x_si, y_si, 'o-', label='Si')
plt.plot(x_ge, y_ge, 's-', label='Ge')
plt.plot(x_sic, y_sic, '^-', label='SiC')
plt.plot(x_insb, y_insb, 'd-', label='InSb')

# Оформление осей
plt.xlabel(r'$1000/T, \text{К}^{-1}$')
plt.ylabel(r'$\ln \gamma_{\text{эксп}}$')
plt.grid(True, which='both', linestyle='--')
plt.legend()

# Сохранение
plt.savefig('semiconductors-conductivity.pgf')