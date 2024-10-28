import math
import numpy as np

Q_values_user = np.array([50, 100, 200, 220, 300, 400]) / 3600  # en m³/s]) / 3600  # en m³/s
H_total_user_values = []

import math

def colebrook_white(D, Re, roughness):
    if Re < 2000:
        return 64 / Re  # Flujo laminar
    else:
        # Flujo turbulento (iterativo)
        f = 0.02  # Valor inicial
        for _ in range(10):  # Iterar para mejorar la aproximación
            f = 1 / (-2 * math.log10((roughness / (3.7 * D)) + (5.74 / (Re * 0.9))))*2
        return f
D_asp = 0.2  # Diámetro de la tubería de aspiración (m)
D_imp = 0.15  # Diámetro de la tubería de impulsión (m)
nu = 0.946e-6  # Viscosidad cinemática del agua (m²/s) 
L_asp = 10  # Longitud de la tubería de aspiración (m)
L_imp = 300  # Longitud de la tubería de impulsión (m)
g = 9.81  # Aceleración de la gravedad (m/s²)
k_sing_asp = 7.7  # Pérdida de carga en la singularidad de aspiración (m)
k_sing_imp =15.98  # Pérdida de carga en la singularidad de impulsión (m)
# Cálculos de alturas para los caudales proporcionados
for Q_i in Q_values_user:
    # Velocidades en las tuberías de aspiración e impulsión
    V_asp_i = Q_i / (math.pi * D_asp**2 / 4)
    V_imp_i = Q_i / (math.pi * D_imp**2 / 4)

    # Número de Reynolds
    Re_asp_i = V_asp_i * D_asp / nu
    Re_imp_i = V_imp_i * D_imp / nu

    # Factor de fricción
    f_asp_i = colebrook_white(D_asp, Re_asp_i,0.15)
    f_imp_i = colebrook_white(D_imp, Re_imp_i,0.15)

    # Pérdidas por fricción en aspiración e impulsión
    hf_asp_i = f_asp_i * (L_asp / D_asp) * (V_asp_i ** 2) / (2 * g)
    hf_imp_i = f_imp_i * (L_imp / D_imp) * (V_imp_i ** 2) / (2 * g)

    # Pérdidas en singularidades
    h_sing_asp_i = k_sing_asp * (V_asp_i ** 2) / (2 * g)
    h_sing_imp_i = k_sing_imp * (V_imp_i ** 2) / (2 * g)

    # Pérdida de carga total
    hf_total_i = hf_asp_i + hf_imp_i + h_sing_asp_i + h_sing_imp_i

    # Altura de bombeo total para este caudal
    H_total_i = 95 + hf_total_i
    H_total_user_values.append(H_total_i)

print(H_total_user_values)


#--------------------------------------------------------------------------------



# Calcular el NPSHD para un caudal de 220 m³/h

# Conversión de caudal de m³/h a m³/s
# Datos constantes para el cálculo directo de NPSHD
P_atm = 101325  # Presión atmosférica en Pa
rho = 1025  # Densidad del agua salada en kg/m³
g = 9.81  # Aceleración de la gravedad en m/s²
P_vapor = 2340  # Presión de vapor del agua en Pa a 18°C
Q = 220 / 3600  # Caudal en m³/s
d_asp = 0.2  # Diámetro de la tubería de aspiración en metros
z_asp = 95  # Altura del nivel de la superficie libre respecto al eje de la bomba en metros
f_asp = 0.02  # Factor de fricción en la línea de aspiración
L_asp = 10  # Longitud de la tubería de aspiración en metros
k_asp_total = 2  # Coeficiente total de pérdida en la línea de aspiración

# Velocidad en la línea de aspiración
V_asp = Q / (math.pi * (d_asp / 2)**2)

# Pérdidas en la línea de aspiración
H_fric_asp = f_asp * (L_asp / d_asp) * (V_asp**2 / (2 * g))
H_perd_asp = H_fric_asp + k_asp_total * (V_asp**2 / (2 * g))

# Cálculo del NPSHD
NPSHD = (P_atm / (rho * g)) + (V_asp**2 / (2 * g)) + z_asp - H_perd_asp - (P_vapor / (rho * g))

print(NPSHD)