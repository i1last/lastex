from lupa import LuaRuntime
import matplotlib.pyplot as plt

# --- Инициализация Lua ---
lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute(f"dofile('code/processing.lua')")
p = lua.globals().p
r = lua.globals().r

# --- Функция для построения векторных диаграмм ---
def build_vector_diagram(U_R, U_X, U0, element_label, filename):
    plt.figure()
    ax = plt.gca()
    
    # Параметры стрелок: увеличенная толщина (width) и размеры головок
    q_params = {
        'angles': 'xy', 
        'scale_units': 'xy', 
        'scale': 1, 
        'color': 'black', 
        'width': 0.006,
        'headwidth': 4, 
        'headlength': 5,
        'pivot': 'tail'
    }
    
    # Отрисовка векторов
    ax.quiver(0, 0, U_R, 0, **q_params)
    ax.quiver(U_R, 0, 0, U_X, **q_params)
    ax.quiver(0, 0, U_R, U_X, linestyle='--', **q_params)

    # Текстовые подписи векторов
    offset = U0 * 0.08
    if filename == 'vd_rlc_1.pgf': offset = U0 * 0.01
    ax.text(U_R / 2, -offset if U_X >= 0 else offset, r"$\vec{U}_R$", fontsize=12, ha='center')
    # Для реактивного вектора подпись смещается в зависимости от его величины
    ax.text(U_R + offset/2, U_X / 2 if abs(U_X) > offset else offset, element_label, fontsize=12, va='center')
    ax.text(U_R / 2, U_X / 2 + (offset if U_X >= 0 else -offset), r"$\vec{U}_0$", fontsize=12, ha='right')

    # Настройка лимитов (предотвращение "сплющивания" при резонансе)
    margin_x = max(abs(U_R), 0.5) * 0.25
    margin_y = max(abs(U_X), 0.5) * 0.25
    
    ax.set_xlim(-margin_x, U_R + margin_x)
    ax.set_ylim(min(0, U_X) - margin_y, max(0, U_X) + margin_y)

    ax.axhline(0, color='black', linewidth=0.8)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.set_xlabel(r"Действительная ось, В")
    ax.set_ylabel(r"Мнимая ось, В")
    # ax.set_aspect('equal', adjustable='box')
    ax.grid(True, linestyle='--', alpha=0.6)
    
    plt.savefig(filename)
    plt.close()

# --- Генерация файлов ---
# RC-цепь
for i in range(1, 3):
    build_vector_diagram(p.RC.U_R[i], -p.RC.U_C[i], p.RC.U0[i], r"$\vec{U}_C$", f"vd_rc_{i}.pgf")

# RL-цепь
for i in range(1, 3):
    build_vector_diagram(p.RL.U_R[i], p.RL.U_L[i], p.RL.U0[i], r"$\vec{U}_L$", f"vd_rl_{i}.pgf")

# RLC-цепь
for i in range(1, 4):
    U_X_val = p.RLC.U_L[i] - p.RLC.U_C[i]
    build_vector_diagram(p.RLC.U_R[i], U_X_val, p.RLC.U0[i], r"$\vec{U}_L - \vec{U}_C$", f"vd_rlc_{i}.pgf")