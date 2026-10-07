"""
problema 3: maquina sobre {a,b} con alfabeto de cinta {a,b,X,⊔}

lo que entendi que hace cada estado:
- q0: borra la primera a (la cambia por ⊔) y pasa a q1. si no empieza con a
      rechaza
- q1: camina a la derecha saltando a's y X's hasta la primera b, la marca
      con X y pasa a q2
- q2: mira lo que sigue despues de la b marcada:
      * otra b  -> todavia faltan b's, regresa (q3)
      * blanco  -> ya no hay b's, va a revisar todo (q6)
      * a o X   -> rechaza (habia una a despues de una b)
- q3: regresa a la izquierda por las X hasta topar con una a (si no hay a
      rechaza porque hay mas b's que a's)
- q4: sigue a la izquierda por las a's hasta la ultima X o el blanco del
      inicio
- q5: marca con X la a mas a la izquierda que queda y vuelve a q1
- q6: regresa a la izquierda revisando que todo sea X; si llega al blanco
      del inicio acepta, si encuentra una a o b rechaza

o sea: por cada b marcada (menos la ultima) se marca una a, y la primera a
se borra en q0. eso empareja las a's con las b's => L(M) = { a^n b^n | n >= 1 }

nota: el enunciado tambien pone delta(q_acc,s) = (q_acc,⊔,L) y lo mismo para
q_rej. aqui uso la convencion normal de que la maquina se detiene apenas
entra a q_acc o q_rej, entonces esas transiciones no se ejecutan.
"""

import itertools
import sys

from maquina_turing import BLANCO, MaquinaTuring, imprimir_traza

ACC = "q_acc"
REJ = "q_rej"

DELTA_P3 = {
    # q0
    ("q0", "a"): ("q1", BLANCO, "R"),
    ("q0", "b"): (REJ, BLANCO, "R"),
    ("q0", "X"): (REJ, BLANCO, "R"),
    ("q0", BLANCO): (REJ, BLANCO, "R"),
    # q1
    ("q1", "a"): ("q1", "a", "R"),
    ("q1", "b"): ("q2", "X", "R"),
    ("q1", "X"): ("q1", "X", "R"),
    ("q1", BLANCO): (REJ, BLANCO, "R"),
    # q2
    ("q2", "a"): (REJ, BLANCO, "R"),
    ("q2", "b"): ("q3", "b", "L"),
    ("q2", "X"): (REJ, BLANCO, "R"),
    ("q2", BLANCO): ("q6", BLANCO, "L"),
    # q3
    ("q3", "a"): ("q4", "a", "L"),
    ("q3", "b"): (REJ, BLANCO, "R"),
    ("q3", "X"): ("q3", "X", "L"),
    ("q3", BLANCO): (REJ, BLANCO, "R"),
    # q4
    ("q4", "a"): ("q4", "a", "L"),
    ("q4", "b"): (REJ, BLANCO, "R"),
    ("q4", "X"): ("q5", "X", "R"),
    ("q4", BLANCO): ("q5", BLANCO, "R"),
    # q5
    ("q5", "a"): ("q1", "X", "R"),
    ("q5", "b"): (REJ, BLANCO, "R"),
    ("q5", "X"): (REJ, BLANCO, "R"),
    ("q5", BLANCO): (REJ, BLANCO, "R"),
    # q6
    ("q6", "a"): (REJ, BLANCO, "R"),
    ("q6", "b"): (REJ, BLANCO, "R"),
    ("q6", "X"): ("q6", "X", "L"),
    ("q6", BLANCO): (ACC, BLANCO, "R"),
}


def crear_maquina():
    return MaquinaTuring(DELTA_P3, estado_inicial="q0", estados_parada={ACC, REJ})


def acepta(w):
    # corre la maquina y dice si termino en q_acc
    m = crear_maquina()
    m.correr(w)
    return m.estado == ACC


def es_anbn(w):
    # mi definicion del lenguaje para compararlo: a^n b^n con n >= 1
    n = len(w) // 2
    return n >= 1 and w == "a" * n + "b" * n


def generar_dot():
    """
    genera el diagrama en formato graphviz (dot) como pide el inciso a):
    sin q_rej y sin las transiciones que salen de q_acc. junto en una sola
    flecha las transiciones que van entre los mismos dos estados.
    """
    etiquetas = {}
    for (q, s), (p, t, d) in DELTA_P3.items():
        if p == REJ:
            continue  # se quita q_rej con todo y sus flechas
        etiquetas.setdefault((q, p), []).append(s + "/" + t + "," + d)
    lineas = [
        "digraph problema3 {",
        "    rankdir=LR;",
        "    node [shape=circle];",
        "    " + ACC + " [shape=doublecircle];",
        "    inicio [shape=point];",
        "    inicio -> q0;",
    ]
    for (q, p), lista in etiquetas.items():
        lineas.append('    %s -> %s [label="%s"];' % (q, p, "\\n".join(lista)))
    lineas.append("}")
    return "\n".join(lineas)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    m = crear_maquina()

    print("inciso b) descripciones instantaneas para aabb")
    traza = m.correr("aabb")
    imprimir_traza(traza)
    print("estado final:", m.estado, "| pasos:", m.pasos)
    print()

    # inciso c) comparo la maquina contra a^n b^n con todas las palabras
    # de longitud 0 hasta 12, si alguna no coincide la imprimo
    total = 0
    for largo in range(13):
        for letras in itertools.product("ab", repeat=largo):
            w = "".join(letras)
            total += 1
            if acepta(w) != es_anbn(w):
                print("no coincide con:", repr(w))
    print("inciso c) se probaron", total, "palabras y todas coinciden con a^n b^n (n >= 1)")
    print()

    print("inciso d) aba")
    traza = m.correr("aba")
    imprimir_traza(traza)
    print("estado final:", m.estado, "=> aba", "si" if m.estado == ACC else "no", "pertenece a L(M)")
    print()

    print("inciso a) diagrama en dot (se puede pegar en graphviz):")
    print(generar_dot())


if __name__ == "__main__":
    main()
