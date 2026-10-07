"""
problema 2: descripciones instantaneas para 100, 10011 y 11

idea de la maquina:
- q0 camina a la derecha hasta el final de la palabra (el primer blanco)
- ahi regresa una casilla y entra a q1
- q1 va sumando 1 desde el bit menos significativo:
    * si lee 1 lo cambia a 0 y sigue a la izquierda (se lleva el acarreo)
    * si lee 0 lo cambia a 1 y para
    * si lee blanco (todos eran 1) escribe blanco y para, o sea el acarreo
      final se pierde y el resultado es suma 1 modulo 2^n

nota: en el pdf la B de delta(q0,B) y delta(q1,B) es el blanco ⊔
"""

import sys

from maquina_turing import BLANCO, MaquinaTuring, imprimir_traza

DELTA_P2 = {
    ("q0", "0"): ("q0", "0", "R"),
    ("q0", "1"): ("q0", "1", "R"),
    ("q0", BLANCO): ("q1", BLANCO, "L"),
    ("q1", "0"): ("q_halt", "1", "R"),
    ("q1", "1"): ("q1", "0", "L"),
    ("q1", BLANCO): ("q_halt", BLANCO, "L"),
}


def crear_maquina():
    return MaquinaTuring(DELTA_P2, estado_inicial="q0", estados_parada={"q_halt"})


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    m = crear_maquina()
    # los tres incisos del problema
    for inciso, w in [("a", "100"), ("b", "10011"), ("c", "11")]:
        traza = m.correr(w)
        print("inciso " + inciso + ") entrada:", w)
        imprimir_traza(traza)
        print("salida:", m.salida(), "| pasos:", m.pasos)
        print()


if __name__ == "__main__":
    main()
