import matplotlib
import matplotlib.pyplot as plt
import lupa
import numpy as np

# --- Инициализация Lua и загрузка данных ---
lua = lupa.LuaRuntime(unpack_returned_tuples=False)
with open('./../protocol.lua', 'r', encoding='utf-8') as f:
    lua_code = f.read()
lua.execute(lua_code)
protocol = lua.globals().protocol

# --- Функция обработки данных ---
def process_intensity_data(raw_data, R_dark):
    """
    Воспроизводит логику расчетов для световой характеристики.
    """
    d_max = 4.0 # мм
    gamma_t = (1 / R_dark) * 1e6
    
    R_c = np.array(list(raw_data.R_c.values()))
    d_vals = np.array(list(raw_data.d.values())) * 1000 # в мм
    
    gamma_c = (1 / R_c) * 1e6
    gamma_f = np.maximum(1e-9, gamma_c - gamma_t) # Избегаем log(0)
    d_rel = d_vals / d_max
    
    # Логарифмы для осей
    log_gamma_f = np.log10(gamma_f)
    log_d_rel = np.log10(d_rel)
    
    return log_d_rel, log_gamma_f

# --- Обработка данных ---
x_data, y_data = process_intensity_data(protocol.Intensity, protocol.DarkResistanceOfCdSe)


# --- Построение графика ---
fig, ax = plt.subplots(figsize=(6, 4.5))

ax.plot(x_data, y_data, marker='o', linestyle='-', markersize=4)

ax.set_xlabel(r'$\lg(d/d_{\max})$')
ax.set_ylabel(r'$\lg \gamma_{\text{ф}}$')
ax.grid(True, linestyle=':', alpha=0.6)

fig.tight_layout()

# --- Сохранение в файл ---
output_filename = 'intensity_plot.pgf'
plt.savefig(output_filename)
print(f"✅ График сохранен в файл: {output_filename}")