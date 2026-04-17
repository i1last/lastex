import numpy as np
import matplotlib.pyplot as plt
from scripts.calc_6 import ex6, reaction
from scripts.calc_1 import n

def plot_meander_reaction(ti, figure_num, index_label):
    # Адаптивный временной интервал: от небольшого отрицательного смещения до 5*ti
    t_min = -0.05 * ti
    t_max = 1.75 * ti
    t = np.linspace(t_min, t_max, 2000)

    # Вычисление реакции цепи
    y_reaction = np.array([reaction(tau, ti) for tau in t])
    
    # Формирование входного двуполярного меандра
    y_input = np.piecewise(t,
        [
            (t < 0),
            (t >= 0) & (t <= 0.5 * ti),
            (t > 0.5 * ti) & (t <= ti)
        ], 
        [
            0,
            ex6['Im'],
            -ex6['Im'],
            0
        ]
    )

    # Настройка графика
    plt.figure(figure_num)
    plt.plot(t, y_input, marker='', label=fr'Входной сигнал $i_1(t)$ при $t_\text{{и}} = {ti}$')
    plt.plot(t, y_reaction, marker='', label=r'Реакция цепи $i_2(t)$')
    plt.xlim(left=t_min)
    plt.xlabel(r'$t$')
    plt.ylabel(r'Ток')
    plt.grid(True)
    plt.legend(ncol=2)
    plt.tight_layout()
    
    # Сохранение в PGF (раскомментировать при необходимости)
    plt.savefig(f'plot_reaction_{index_label}.pgf')

# 1. Построение графика для воздействия с длительностью t_i1
plot_meander_reaction(n['ti1'], 1, 'i1')

# 2. Построение графика для воздействия с длительностью t_i2
plot_meander_reaction(n['ti2'], 2, 'i2')

# Отображение всех созданных фигур
# plt.show()