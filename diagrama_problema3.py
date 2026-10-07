"""
dibuja el diagrama de control de estados del problema 3 como un svg.

siguiendo el hint, q1 a q5 van en un pentagono. q0 queda afuera a la
izquierda de q1, y q6 con q_acc a la derecha. no dibujo q_rej ni las
transiciones que salen de q_acc (como pide el inciso a).

las flechas y etiquetas las saco directo de DELTA_P3 para no equivocarme
copiando a mano.
"""

import math

from problema3 import ACC, DELTA_P3, REJ

RADIO_NODO = 26

# posiciones de cada estado en el dibujo (x, y)
CENTRO = (430, 330)
R_PENT = 170


def _vertice_pentagono(k):
    # k = 0 es el de arriba y luego avanzo en el sentido del reloj
    ang = math.radians(-90 + 72 * k)
    return (CENTRO[0] + R_PENT * math.cos(ang), CENTRO[1] + R_PENT * math.sin(ang))


POS = {
    "q1": _vertice_pentagono(0),
    "q2": _vertice_pentagono(1),
    "q3": _vertice_pentagono(2),
    "q4": _vertice_pentagono(3),
    "q5": _vertice_pentagono(4),
    "q0": (130, 160),
    "q6": (760, 230),
    ACC: (900, 400),
}


def _juntar_etiquetas():
    # agrupo las transiciones que van del mismo estado al mismo estado
    flechas = {}
    for (q, s), (p, t, d) in DELTA_P3.items():
        if p == REJ:
            continue
        flechas.setdefault((q, p), []).append(s + "/" + t + "," + d)
    return flechas


def _texto(x, y, lineas, ancla="middle"):
    # escribe varias lineas de texto centradas en (x, y)
    partes = []
    alto = 15
    y0 = y - alto * (len(lineas) - 1) / 2
    for i, linea in enumerate(lineas):
        partes.append(
            '<text x="%.1f" y="%.1f" text-anchor="%s" dominant-baseline="middle">%s</text>'
            % (x, y0 + i * alto, ancla, linea)
        )
    return "\n".join(partes)


def _flecha_recta(a, b, lineas):
    # linea de borde a borde de los circulos, con la etiqueta a un lado
    (x1, y1), (x2, y2) = POS[a], POS[b]
    dx, dy = x2 - x1, y2 - y1
    dist = math.hypot(dx, dy)
    ux, uy = dx / dist, dy / dist
    sx, sy = x1 + ux * RADIO_NODO, y1 + uy * RADIO_NODO
    ex, ey = x2 - ux * RADIO_NODO, y2 - uy * RADIO_NODO
    # la etiqueta va en medio, movida un poco hacia afuera (normal a la linea)
    mx, my = (sx + ex) / 2, (sy + ey) / 2
    nx, ny = uy, -ux
    # para el pentagono quiero las etiquetas hacia afuera del centro
    if (mx + nx - CENTRO[0]) ** 2 + (my + ny - CENTRO[1]) ** 2 < (mx - CENTRO[0]) ** 2 + (my - CENTRO[1]) ** 2:
        nx, ny = -nx, -ny
    sep = 14 + 8 * len(lineas)
    linea = '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" marker-end="url(#punta)"/>' % (sx, sy, ex, ey)
    return linea + "\n" + _texto(mx + nx * sep, my + ny * sep, lineas)


def _bucle(q, lineas):
    # un lazo encima del estado, apuntando hacia afuera del pentagono
    x, y = POS[q]
    ang = math.atan2(y - CENTRO[1], x - CENTRO[0])
    if q in ("q6",):
        ang = math.radians(-90)  # q6 lo dejo con el lazo arriba
    a1, a2 = ang - 0.5, ang + 0.5
    p1 = (x + RADIO_NODO * math.cos(a1), y + RADIO_NODO * math.sin(a1))
    p2 = (x + RADIO_NODO * math.cos(a2), y + RADIO_NODO * math.sin(a2))
    c1 = (x + 75 * math.cos(a1 - 0.3), y + 75 * math.sin(a1 - 0.3))
    c2 = (x + 75 * math.cos(a2 + 0.3), y + 75 * math.sin(a2 + 0.3))
    camino = '<path d="M %.1f %.1f C %.1f %.1f %.1f %.1f %.1f %.1f" fill="none" marker-end="url(#punta)"/>' % (
        p1[0], p1[1], c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
    tx = x + (62 + 8 * len(lineas)) * math.cos(ang)
    ty = y + (62 + 8 * len(lineas)) * math.sin(ang)
    return camino + "\n" + _texto(tx, ty, lineas)


def generar_svg():
    piezas = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="560" viewBox="0 0 1000 560" '
        'font-family="monospace" font-size="13">',
        '<rect width="100%" height="100%" fill="white"/>',
        "<defs><marker id=\"punta\" markerWidth=\"10\" markerHeight=\"10\" refX=\"9\" refY=\"5\" "
        "orient=\"auto\"><path d=\"M0,0 L10,5 L0,10 z\" fill=\"black\"/></marker></defs>",
        '<g stroke="black" stroke-width="1.5" fill="black">',
    ]
    # flecha de entrada a q0
    x0, y0 = POS["q0"]
    piezas.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" marker-end="url(#punta)"/>'
                  % (x0 - 80, y0, x0 - RADIO_NODO, y0))
    piezas.append("</g>")

    # las transiciones (las lineas van con stroke, el texto sin stroke)
    for (q, p), lineas in _juntar_etiquetas().items():
        if q == p:
            pieza = _bucle(q, lineas)
        else:
            pieza = _flecha_recta(q, p, lineas)
        piezas.append('<g stroke="black" stroke-width="1.5" fill="none">' + pieza.replace(
            "<text", '<text stroke="none" fill="black"') + "</g>")

    # los circulos de los estados encima de todo
    for q, (x, y) in POS.items():
        piezas.append('<circle cx="%.1f" cy="%.1f" r="%d" fill="white" stroke="black" stroke-width="1.5"/>'
                      % (x, y, RADIO_NODO))
        if q == ACC:
            piezas.append('<circle cx="%.1f" cy="%.1f" r="%d" fill="none" stroke="black" stroke-width="1.5"/>'
                          % (x, y, RADIO_NODO - 5))
        piezas.append(_texto(x, y, [q]))
    piezas.append("</svg>")
    return "\n".join(piezas)


if __name__ == "__main__":
    with open("diagrama_problema3.svg", "w", encoding="utf-8") as f:
        f.write(generar_svg())
    print("listo, se genero diagrama_problema3.svg")
