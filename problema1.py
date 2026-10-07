"""
problema 1: que funcion calcula la maquina sobre {a,b,A,B}*

interpretacion que tome:
- la "B" del diagrama es la letra mayuscula B del alfabeto (no el blanco),
  porque si fuera el blanco la transicion B/b,R nunca dejaria de escribir b's
  y la maquina no terminaria
- el "ε" de la transicion 0 -> 1 lo tomo como leer el blanco ⊔ (o sea cuando
  ya se acabo la palabra), escribe blanco y se mueve a la derecha
- el estado 1 (doble circulo) es el de parada / aceptacion
"""

import sys

from maquina_turing import BLANCO, MaquinaTuring, imprimir_traza

# tabla de transiciones tal cual del diagrama
DELTA_P1 = {
    ("0", "A"): ("0", "a", "R"),
    ("0", "B"): ("0", "b", "R"),
    ("0", "a"): ("0", "a", "R"),
    ("0", "b"): ("0", "b", "R"),
    ("0", BLANCO): ("1", BLANCO, "R"),
}


def crear_maquina():
    return MaquinaTuring(DELTA_P1, estado_inicial="0", estados_parada={"1"})


def main():
    # para que la consola de windows pueda imprimir ⊔ y ⊢
    sys.stdout.reconfigure(encoding="utf-8")
    m = crear_maquina()
    # unos ejemplos para ver que hace la maquina
    for w in ["", "a", "AbBa", "ABAB", "abab", "BaAb"]:
        traza = m.correr(w)
        print("entrada:", repr(w))
        imprimir_traza(traza)
        print("salida :", repr(m.salida()), "| estado final:", m.estado)
        # la salida siempre es la misma palabra pero en minusculas
        assert m.salida() == w.lower()
        print()
    print("conclusion: f(w) = w con todas las mayusculas pasadas a minusculas")


if __name__ == "__main__":
    main()
