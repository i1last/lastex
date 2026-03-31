import numpy as np
from scripts.calc_2 import tf

fact = {
    'K': tf['N2'] / tf['D3'],
    'alpha1': -tf['p1_re'],
    'alpha2': -tf['p2_re'],
    'beta2': tf['p2_im'],
    'omega0_sq': tf['z1_im']**2
}

freq = {}
freq['A0'] = tf['N0'] / tf['D0']

def get_h_factored(w):
    s = 1j * w
    num = tf['N2'] * s**2 + tf['N0']
    den = tf['D3'] * s**3 + tf['D2'] * s**2 + tf['D1'] * s + tf['D0']
    h = num / den
    return np.abs(h), np.angle(h)

freq['w1'] = 0
freq['A1'], freq['Phi1'] = get_h_factored(freq['w1'])

freq['w2'] = tf['z1_im']
freq['A2'], freq['Phi2'] = get_h_factored(freq['w2'])

freq['level'] = 0.707 * freq['A0']
freq['w_c'] = 0.45 
freq['td'] = np.radians(25) / 0.5