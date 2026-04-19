import numpy as np
import matplotlib.pyplot as plt
from scripts.calc import p

t = np.array(p['rt']['t'])

materials =[
    ('R_Cu', 'Медь', 's'),
    ('R_Ni', 'Никель', 'o'),
    ('R_Const', 'Константан', '^')
]

for key, label, marker in materials:
    R = np.array(p['rt'][key])
    
    # Аппроксимирующая прямая (касательная)
    poly = np.polyfit(t, R, 1)
    t_fit = np.linspace(min(t), max(t), 100)
    R_fit = np.polyval(poly, t_fit)
    
    # Отрисовка экспериментальных точек и прямой
    p_line = plt.plot(t, R, marker=marker, linestyle='None', label=label)[0]
    color = p_line.get_color()
    plt.plot(t_fit, R_fit, color=color, linestyle='-', marker='', label="Аппроксимация")
    
    # Отрисовка прямоугольного треугольника для демонстрации отношения dR/dt
    t1, t2 = 30, 125
    R1, R2 = np.polyval(poly, t1), np.polyval(poly, t2)
    plt.plot([t1, t2, t2], [R1, R1, R2], color=color, linestyle='--', marker='')
    
    plt.xlabel(r'$t$, $^\circ$C')
    plt.ylabel(r'$R$, Ом')
    plt.legend(ncol=2, numpoints=1)
    plt.savefig(f'plot_rt_{key}.pgf')
    plt.close()
