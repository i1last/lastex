import numpy as np
from lupa import LuaRuntime
import matplotlib.pyplot as plt

lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute("dofile('code/3.lua')")
tf = lua.globals().tf

w = np.logspace(-2, 1, 500)

def get_response(w_arr):
    n_val = tf.N0 - tf.N2 * w_arr**2
    d_val = (tf.D0 - tf.D2 * w_arr**2) + 1j * (tf.D1 * w_arr - tf.D3 * w_arr**3)
    h = n_val / d_val
    return np.abs(h), np.angle(h)

a_w, phi_w = get_response(w)

# График АЧХ
plt.figure()
plt.plot(w, a_w, marker="")
plt.axhline(y=0.707*a_w[0], color='r', linestyle='--')
plt.xlabel(r'$\omega$')
plt.ylabel(r'$A(\omega)$')
plt.savefig('plot_afc.pgf')

# График ФЧХ
plt.figure()
plt.plot(w, np.degrees(phi_w), marker="")
plt.xlabel(r'$\omega$')
plt.ylabel(r'$\Phi(\omega), {}^{\circ}$')
plt.savefig('plot_pfc.pgf')

# Годограф (АФХ)
plt.figure()
plt.plot(a_w * np.cos(phi_w), a_w * np.sin(phi_w), marker="")
plt.xlabel('Re')
plt.ylabel('Im')
plt.savefig('plot_afh.pgf')