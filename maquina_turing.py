"""
simulador sencillo de una maquina de turing determinista de una sola cinta.

lo uso para comprobar a mano los problemas del laboratorio 9, o sea para
sacar las descripciones instantaneas y ver que salida deja la maquina.

convenciones que use:
- la cinta es infinita para los dos lados (por eso la guardo en un dict
  posicion -> simbolo, asi no me preocupo por indices negativos)
- el blanco se representa con el simbolo ⊔
- una transicion es delta[(estado, simbolo)] = (estado_nuevo, escribe, mov)
  donde mov es "R" (derecha) o "L" (izquierda)
- la maquina se detiene apenas entra a un estado de parada (q_halt, q_acc,
  q_rej, etc) o cuando no hay transicion definida para (estado, simbolo)
"""

BLANCO = "⊔"


class MaquinaTuring:
    def __init__(self, delta, estado_inicial, estados_parada, blanco=BLANCO):
        # guardo la tabla de transiciones y los estados importantes
        self.delta = delta
        self.estado_inicial = estado_inicial
        self.estados_parada = set(estados_parada)
        self.blanco = blanco
        self.reiniciar("")

    def reiniciar(self, entrada):
        # pongo la entrada en la cinta empezando en la posicion 0
        # y el cabezal arranca en el primer simbolo de la entrada
        self.cinta = {i: s for i, s in enumerate(entrada)}
        self.cabezal = 0
        self.estado = self.estado_inicial
        self.pasos = 0

    def leer(self):
        # si la casilla nunca se escribio entonces es blanco
        return self.cinta.get(self.cabezal, self.blanco)

    def esta_detenida(self):
        # se detiene si llego a un estado de parada o si no hay transicion
        if self.estado in self.estados_parada:
            return True
        return (self.estado, self.leer()) not in self.delta

    def paso(self):
        # aplica una sola transicion: escribir, mover y cambiar de estado
        simbolo = self.leer()
        estado_nuevo, escribe, mov = self.delta[(self.estado, simbolo)]
        self.cinta[self.cabezal] = escribe
        if mov == "R":
            self.cabezal += 1
        elif mov == "L":
            self.cabezal -= 1
        else:
            raise ValueError("movimiento invalido: " + str(mov))
        self.estado = estado_nuevo
        self.pasos += 1

    def _rango_visible(self):
        # busco desde el primer hasta el ultimo simbolo que no es blanco,
        # pero siempre incluyendo donde esta el cabezal para que se vea
        no_blancos = [i for i, s in self.cinta.items() if s != self.blanco]
        posiciones = no_blancos + [self.cabezal]
        return min(posiciones), max(posiciones)

    def descripcion_instantanea(self):
        # formato u q v: lo que esta a la izquierda del cabezal, el estado,
        # y despues desde el simbolo que se esta leyendo hacia la derecha
        izq, der = self._rango_visible()
        u = "".join(self.cinta.get(i, self.blanco) for i in range(izq, self.cabezal))
        v = "".join(self.cinta.get(i, self.blanco) for i in range(self.cabezal, der + 1))
        return u + " " + self.estado + " " + v

    def salida(self):
        # la salida es el contenido de la cinta quitando los blancos de las
        # orillas (los blancos de en medio si se quedan)
        no_blancos = [i for i, s in self.cinta.items() if s != self.blanco]
        if not no_blancos:
            return ""
        izq, der = min(no_blancos), max(no_blancos)
        return "".join(self.cinta.get(i, self.blanco) for i in range(izq, der + 1))

    def correr(self, entrada, max_pasos=10000):
        """
        corre la maquina con la entrada dada y regresa la lista de todas las
        descripciones instantaneas (incluyendo la inicial y la final).
        max_pasos es solo para no quedarme en un ciclo infinito por error.
        """
        self.reiniciar(entrada)
        traza = [self.descripcion_instantanea()]
        while not self.esta_detenida():
            if self.pasos >= max_pasos:
                raise RuntimeError("la maquina no se detuvo en " + str(max_pasos) + " pasos")
            self.paso()
            traza.append(self.descripcion_instantanea())
        return traza


def imprimir_traza(traza):
    # imprime las descripciones separadas con el simbolo de "produce"
    for i, di in enumerate(traza):
        prefijo = "    " if i == 0 else " ⊢  "
        print(prefijo + di)
