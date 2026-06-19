import numpy as np

obstaculos = [
    (-8.0708,  5.0407, 13.6385, 6.8192),
    (13.2276,  5.0495, 13.6385, 6.8192),
    (13.2276, -5.8435, 13.6385, 6.8192),
    (-8.0708, -5.8435, 13.6385, 6.8192),
]
margen = 8.0
escala = 0.7
centro_x = 0.0
centro_y = 0.0

def hoja_cuadrante(cx, cy, w, h, entrada, salida):
    left   = cx - w/2 - margen
    right  = cx + w/2 + margen
    bottom = cy - h/2 - margen
    top    = cy + h/2 + margen
    p_top    = np.array([cx, top])
    p_right  = np.array([right, cy])
    p_bottom = np.array([cx, bottom])
    p_left   = np.array([left, cy])
    if cx < 0 and cy > 0:      # sup izq
        puntos = [entrada, p_left, p_top, p_right, p_bottom, salida]
    elif cx > 0 and cy > 0:    # sup der
        puntos = [entrada, p_top, p_right, p_bottom, p_left, salida]
    elif cx > 0 and cy < 0:    # inf der
        puntos = [entrada, p_right, p_bottom, p_left, p_top, salida]
    else:                       # inf izq
        puntos = [entrada, p_bottom, p_left, p_top, p_right, salida]
    return puntos

# Entradas y salidas de cada hoja pasando por el origen
# Hoja 0 (sup izq): entra desde origen hacia izq-arriba, sale hacia der-arriba
# Hoja 1 (sup der): entra desde origen hacia der-arriba, sale hacia der-abajo
# Hoja 2 (inf der): entra desde origen hacia der-abajo, sale hacia izq-abajo
# Hoja 3 (inf izq): entra desde origen hacia izq-abajo, sale hacia origen

entradas = [
    np.array([0.0, 0.0]),
    np.array([0.0, 0.0]),
    np.array([0.0, 0.0]),
    np.array([0.0, 0.0]),
]
salidas = [
    np.array([0.0, 0.0]),
    np.array([0.0, 0.0]),
    np.array([0.0, 0.0]),
    np.array([0.0, 0.0]),
]

orden_obs = [obstaculos[0], obstaculos[1], obstaculos[2], obstaculos[3]]
tramo_num = 0

for idx, (cx, cy, w, h) in enumerate(orden_obs):
    puntos = hoja_cuadrante(cx, cy, w, h, entradas[idx], salidas[idx])
    n = len(puntos)
    for i in range(n-1):
        p0 = np.array(puntos[i])
        p1 = np.array(puntos[i+1])
        prev = np.array(puntos[i-1]) if i > 0 else p0
        nxt  = np.array(puntos[i+2]) if i+2 < n else p1
        v0 = escala * (p1 - prev)
        v1 = escala * (nxt - p0)
        # Corregir tangentes en origen para dar dirección correcta
        if i == 0:  # primer tramo de la hoja
            dir_salida = np.array(puntos[1]) - np.array([0,0])
            norm = np.linalg.norm(dir_salida)
            if norm > 0:
                v0 = dir_salida / norm * 5.0
        if i == n-2:  # ultimo tramo de la hoja
            dir_entrada = np.array([0,0]) - np.array(puntos[-2])
            norm = np.linalg.norm(dir_entrada)
            if norm > 0:
                v1 = dir_entrada / norm * 5.0
        print(f'        case {tramo_num}; P0=[{p0[0]:.3f},{p0[1]:.3f}]; P1=[{p1[0]:.3f},{p1[1]:.3f}]; V0=[{v0[0]:.3f},{v0[1]:.3f}]; V1=[{v1[0]:.3f},{v1[1]:.3f}];')
        tramo_num += 1

print(f'% Total: {tramo_num} tramos')
