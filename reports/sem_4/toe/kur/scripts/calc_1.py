from scripts.source import s

rec = {
    'omega_base': 1e6,
    'R_base': s['R1'],
}

n = {
    'R1': s['R1'] / rec['R_base'],
    'L1': s['L1'] * rec['omega_base'] / rec['R_base'],
    'L2': s['L2'] * rec['omega_base'] / rec['R_base'],
    'C1': s['C1'] * rec['R_base'] * rec['omega_base'],
    'ti': s['ti'] * rec['omega_base'],
    'ti1': s['ti1'] * rec['omega_base'],
    'ti2': s['ti2'] * rec['omega_base'],
}
n['R2'] = n['R1']