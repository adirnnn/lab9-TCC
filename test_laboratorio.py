"""
pruebas para revisar que las respuestas del laboratorio salen bien.
se corren con: python -m unittest -v
"""

import itertools
import unittest

import problema1
import problema2
import problema3


class TestProblema1(unittest.TestCase):
    def test_pasa_todo_a_minusculas(self):
        # pruebo todas las palabras de {a,b,A,B} hasta largo 5
        m = problema1.crear_maquina()
        for largo in range(6):
            for letras in itertools.product("abAB", repeat=largo):
                w = "".join(letras)
                m.correr(w)
                self.assertEqual(m.estado, "1")
                self.assertEqual(m.salida(), w.lower())


class TestProblema2(unittest.TestCase):
    def setUp(self):
        self.m = problema2.crear_maquina()

    def test_inciso_a(self):
        traza = self.m.correr("100")
        self.assertEqual(traza[-1], "101 q_halt ⊔")
        self.assertEqual(self.m.salida(), "101")

    def test_inciso_b(self):
        traza = self.m.correr("10011")
        self.assertEqual(traza[-1], "101 q_halt 00")
        self.assertEqual(self.m.salida(), "10100")

    def test_inciso_c(self):
        traza = self.m.correr("11")
        self.assertEqual(len(traza), 7)
        self.assertEqual(self.m.salida(), "00")

    def test_suma_uno_modulo(self):
        # en general la maquina suma 1 modulo 2^n (n = largo de la entrada)
        for largo in range(1, 8):
            for bits in itertools.product("01", repeat=largo):
                w = "".join(bits)
                self.m.correr(w)
                esperado = format((int(w, 2) + 1) % (2 ** largo), "0" + str(largo) + "b")
                self.assertEqual(self.m.salida().rjust(largo, "0"), esperado)


class TestProblema3(unittest.TestCase):
    def test_traza_aabb(self):
        m = problema3.crear_maquina()
        traza = m.correr("aabb")
        self.assertEqual(len(traza), 16)
        self.assertEqual(traza[-1], " q_acc XXX")
        self.assertEqual(m.estado, problema3.ACC)

    def test_lenguaje_anbn(self):
        for largo in range(11):
            for letras in itertools.product("ab", repeat=largo):
                w = "".join(letras)
                self.assertEqual(problema3.acepta(w), problema3.es_anbn(w), w)

    def test_aba_no_pertenece(self):
        self.assertFalse(problema3.acepta("aba"))


if __name__ == "__main__":
    unittest.main()
