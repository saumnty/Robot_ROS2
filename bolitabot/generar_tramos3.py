import numpy as np

obstaculos = [
    (-8.0708,  5.0407, 13.6385, 6.8192),
    (13.2276,  5.0495, 13.6385, 6.8192),
    (13.2276, -5.8435, 13.6385, 6.8192),
    (-8.0708, -5.8435, 13.6385, 6.8192),
]
margen = 4.0  # margen moderado
escala = 0.7
centro_x = 2.58
centro_y = -0.40
factor = 3.0  # TRIPLE de tamaño

def hoja_cuadrante(cx, cy, w, h):
    left   = cx - w/2 - margen
    right  = cx + w/2 + margen
    bottom = cy - h/2 - margen
    top    = cy + h/2 + margen
    dx = np.sign(cx - centro_x)
    dy = np.sign(cy - centro_y)
    # Entrada escalada al triple
    entrada = np.array([centro_x + dx*4.0*factor, centro_y + dy*3.5*factor])
    p_top    = np.array([cx*factor, top*factor])
    p_right  = np.array([right*factor, cy*factor])
    p_bottom = np.array([cx*factor, bottom*factor])
    p_left   = np.array([left*factor, cy*factor])
    if cx < centro_x and cy > centro_y:
        puntos = [entrada, p_left, p_top, p_right, p_bottom, entrada]
    elif cx > centro_x and cy > centro_y:
        puntos = [entrada, p_top, p_right, p_bottom, p_left, entrada]
    elif cx > centro_x and cy < centro_y:
        puntos = [entrada, p_right, p_bottom, p_left, p_top, entrada]
    else:
        puntos = [entrada, p_bottom, p_left, p_top, p_right, entrada]
    return puntos

orden_obs = [obstaculos[0], obstaculos[1], obstaculos[2], obstaculos[3]]
tramo_num = 0

# Tramo 0: origen al primer punto
cx0, cy0, w0, h0 = orden_obs[0]
puntos0 = hoja_cuadrante(cx0, cy0, w0, h0)
inicio = np.array(puntos0[0])
d = inicio / np.linalg.norm(inicio)
print(f'        case 0;  P0=[0.000,0.000]; P1=[{inicio[0]:.3f},{inicio[1]:.3f}]; V0=[{d[0]*5:.3f},{d[1]*5:.3f}]; V1=[{d[0]*5:.3f},{d[1]*5:.3f}];')
tramo_num += 1

for idx, (cx, cy, w, h) in enumerate(orden_obs):
    puntos = hoja_cuadrante(cx, cy, w, h)
    n = len(puntos)
    for i in range(n-1):
        p0 = np.array(puntos[i])
        p1 = np.array(puntos[i+1])
        prev = np.array(puntos[i-1]) if i > 0 else p0
        nxt  = np.array(puntos[i+2]) if i+2 < n else p1
        v0 = escala * (p1 - prev)
        v1 = escala * (nxt - p0)
        print(f'        case {tramo_num}; P0=[{p0[0]:.3f},{p0[1]:.3f}]; P1=[{p1[0]:.3f},{p1[1]:.3f}]; V0=[{v0[0]:.3f},{v0[1]:.3f}]; V1=[{v1[0]:.3f},{v1[1]:.3f}];')
        tramo_num += 1
    if idx < 3:
        ultimo = np.array(puntos[-1])
        cx2, cy2, w2, h2 = orden_obs[idx+1]
        puntos2 = hoja_cuadrante(cx2, cy2, w2, h2)
        primero = np.array(puntos2[0])
        d = primero - ultimo
        norm = np.linalg.norm(d)
        if norm > 0: d = d/norm
        v = d * 3.0
        print(f'        case {tramo_num}; P0=[{ultimo[0]:.3f},{ultimo[1]:.3f}]; P1=[{primero[0]:.3f},{primero[1]:.3f}]; V0=[{v[0]:.3f},{v[1]:.3f}]; V1=[{v[0]:.3f},{v[1]:.3f}];')
        tramo_num += 1

ultimo = np.array(hoja_cuadrante(*orden_obs[-1])[-1])
primero = np.array(hoja_cuadrante(*orden_obs[0])[0])
d = primero - ultimo
norm = np.linalg.norm(d)
if norm > 0: d = d/norm
v = d * 3.0
print(f'        case {tramo_num}; P0=[{ultimo[0]:.3f},{ultimo[1]:.3f}]; P1=[{primero[0]:.3f},{primero[1]:.3f}]; V0=[{v[0]:.3f},{v[1]:.3f}]; V1=[{v[0]:.3f},{v[1]:.3f}];')
print(f'% Total: {tramo_num+1} tramos')
