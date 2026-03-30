# code/plot.py
from lupa import LuaRuntime
import matplotlib.pyplot as plt

lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute("dofile('code/processing.lua')")
p = lua.globals().p
r = lua.globals().r

def plot_errors(x_data, delta_data, gamma_data, xlabel, filename):
    fig, ax = plt.subplots()
    ax.plot(list(x_data.values()), list(delta_data.values()), marker='o', label=r'$\delta(x)$')
    ax.plot(list(x_data.values()), list(gamma_data.values()), marker='s', label=r'$\gamma(x)$')
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Погрешность, %')
    ax.legend(ncol=2)
    plt.savefig(filename)
    plt.close()

# 1. Графики погрешностей VDC
plot_errors(p.vdc.x, r.vdc.delta, r.vdc.gamma, 'Напряжение, В', 'vdc_errors.pgf')

# 2. Графики погрешностей VAC
plot_errors(p.vac.x, r.vac.delta, r.vac.gamma, 'Напряжение, В', 'vac_errors.pgf')

# 3. Графики погрешностей IDC (перевод в мА для оси X)
x_idc_ma =[val * 1000 for val in list(p.idc.x.values())]
fig, ax = plt.subplots()
ax.plot(x_idc_ma, list(r.idc.delta.values()), marker='o', label=r'$\delta(x)$')
ax.plot(x_idc_ma, list(r.idc.gamma.values()), marker='s', label=r'$\gamma(x)$')
ax.set_xlabel('Ток, мА')
ax.set_ylabel('Погрешность, %')
ax.legend(ncol=2)
plt.savefig('idc_errors.pgf')
plt.close()

# 4. График АЧХ
fig, ax = plt.subplots()
ax.plot(list(p.afc.f.values()), list(r.afc.K.values()), marker='o', color='black')
ax.axhline(y=0.9, color='red', linestyle='--', label='Уровень 0.9')
ax.set_xscale('log')
ax.set_xlabel('Частота $f$, Гц')
ax.set_ylabel('Коэффициент передачи $K(f)$')
ax.legend(ncol=2)
plt.savefig('afc.pgf')
plt.close()