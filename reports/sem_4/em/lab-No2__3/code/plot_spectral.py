import matplotlib
import matplotlib.pyplot as plt
import lupa
import numpy as np

# --- Настройка Matplotlib для вывода в PGF (для LaTeX) ---
# matplotlib.use("pgf")
# matplotlib.rcParams.update({
#     "pgf.texsystem": "pdflatex",
#     'font.family': 'serif',
#     'text.usetex': True,
#     'pgf.rcfonts': False,
#     'pgf.preamble': r'\usepackage[T2A]{fontenc}\usepackage[utf8]{inputenc}\usepackage{amsmath}'
# })

# --- Инициализация Lua и загрузка данных ---
lua = lupa.LuaRuntime(unpack_returned_tuples=False)
with open('./../protocol.lua', 'r', encoding='utf-8') as f:
    lua_code = f.read()
lua.execute(lua_code)
protocol = lua.globals().protocol

# --- Функция обработки данных ---
def process_spectral_data(raw_data, R_dark):
    """
    Воспроизводит логику расчетов из processing.lua для получения
    относительной фотопроводимости.
    """
    # Темновая проводимость в мкСм
    gamma_t = (1 / R_dark) * 1e6
    
    # LuaTable в Python list
    R_c = np.array(list(raw_data.R_c.values()))
    E_lambda = np.array(list(raw_data.E_lambda.values()))
    lambda_vals = np.array(list(raw_data['lambda'].values())) * 1e6 # в мкм

    # Расчеты
    gamma_c = (1 / R_c) * 1e6
    gamma_f = np.maximum(0, gamma_c - gamma_t)
    gamma_f_prime = gamma_f / E_lambda
    
    max_prime = np.max(gamma_f_prime)
    rel_gamma = gamma_f_prime / max_prime
    
    return lambda_vals, rel_gamma

# --- Обработка для каждого материала ---
lambda_cds, rel_cds = process_spectral_data(protocol.SpectralCdS, protocol.DarkResistanceOfCdS)
lambda_cdse, rel_cdse = process_spectral_data(protocol.SpectralCdSe, protocol.DarkResistanceOfCdSe)

# --- Построение графика ---
fig, ax = plt.subplots(figsize=(6, 4))

ax.plot(lambda_cds, rel_cds, label='CdS', linestyle='--', color='blue')
ax.plot(lambda_cdse, rel_cdse, label='CdSe', color='red')

# Горизонтальная линия для определения красной границы
ax.axhline(y=0.5, color='gray', linestyle='--', linewidth=0.8)
ax.text(np.min(lambda_cds), 0.51, '0.5', va='bottom', ha='left', color='gray')

ax.set_xlabel(r'$\lambda$, мкм')
ax.set_ylabel(r"$\gamma'_{\text{ф}} / \gamma'_{\text{ф}\max}$")
ax.legend()
ax.grid(True, linestyle=':', alpha=0.6)
ax.set_xlim(left=0.45)
ax.set_ylim(bottom=0)

fig.tight_layout()

# --- Сохранение в файл ---
output_filename = 'spectral_plot.pgf'
plt.savefig(output_filename)