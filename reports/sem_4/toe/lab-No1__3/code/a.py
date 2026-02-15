import matplotlib.pyplot as plt
import numpy as np

# 2. Данные (масштабирование: 1 единица = 1000 с^-1)
# Теория: p = -10000 -> -10.0
# Эксперимент: p = -11513 -> -11.51
p_theor = -10.0
p_exp = -11.513

# 3. Настройка графика
# Используем соотношение сторон, удобное для отображения одномерных данных
fig, ax = plt.subplots(figsize=(6, 2.5))

# Отрисовка оси абсцисс (Re)
ax.axhline(0, color='black', linewidth=0.8)

# 4. Нанесение точек
# Теория - синий круг
ax.plot(p_theor, 0, 'bo', label=r'Теория ($p = -10$)', zorder=3)
# Эксперимент - красный крест
ax.plot(p_exp, 0, 'rx', markeredgewidth=2, markersize=8, label=r'Эксперимент ($p \approx -11.5$)', zorder=3)

# 5. Визуализация погрешности (опционально, для наглядности)
# Рисуем стрелку между точками
ax.annotate('', xy=(p_theor, 0), xytext=(p_exp, 0),
            arrowprops=dict(arrowstyle='<->', color='gray', lw=1, shrinkA=5, shrinkB=5))
# Подпись величины погрешности
mid_point = (p_theor + p_exp) / 2
# ax.text(mid_point, 0.4, r'$\delta \approx 13\%$', ha='center', va='bottom', fontsize=9)

# 6. Оформление осей
ax.set_xlabel(r'$\text{Re}(p), \times 10^3 \text{ c}^{-1}$')
ax.set_title(r'')
ax.grid(True, which='both', linestyle='--', alpha=0.5)

# Так как мнимая часть равна 0, ограничиваем ось Y, чтобы график не был пустым
ax.set_ylim(-1.5, 2.0)
ax.set_yticks([]) # Скрываем тики по оси Y, так как они не несут информации
ax.legend(loc='upper left')

# 7. Сохранение
# bbox_inches='tight' убирает лишние белые поля
fig.savefig('a.pgf', bbox_inches='tight')