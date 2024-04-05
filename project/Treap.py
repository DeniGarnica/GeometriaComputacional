import random

class Nodo:
    def __init__(self, clave, prioridad=None):
        self.clave = clave
        self.prioridad = prioridad if prioridad is not None else random.random()
        self.izquierda = None
        self.derecha = None

class Treap:
    def __init__(self):
        self.raiz = None

    def insertar(self, clave, prioridad=None):
        if not self.raiz:
            self.raiz = Nodo(clave, prioridad)
        else:
            self.raiz = self._insertar(self.raiz, clave, prioridad)

    def _insertar(self, nodo, clave, prioridad):
        if not nodo:
            return Nodo(clave, prioridad)

        # Esto es lo que hay que mover, el como se define el orden
        if clave < nodo.clave:
            nodo.izquierda = self._insertar(nodo.izquierda, clave, prioridad)
            if nodo.izquierda.prioridad > nodo.prioridad:
                nodo = self.rotar_derecha(nodo)
        else:
            nodo.derecha = self._insertar(nodo.derecha, clave, prioridad)
            if nodo.derecha.prioridad > nodo.prioridad:
                nodo = self.rotar_izquierda(nodo)
        return nodo

    def rotar_derecha(self, y):
        x = y.izquierda
        T2 = x.derecha
        x.derecha = y
        y.izquierda = T2
        return x

    def rotar_izquierda(self, x):
        y = x.derecha
        T2 = y.izquierda
        y.izquierda = x
        x.derecha = T2
        return y

    # Método para imprimir el Treap (Para propósitos de depuración y visualización)
    def imprimir(self, nodo=None, nivel=0, prefijo="Raíz: "):
        if nodo is None:
            nodo = self.raiz

        print(" " * nivel * 2 + prefijo + str(nodo.clave) + " (" + str(nodo.prioridad) + ")")
        if nodo.izquierda is not None:
            self.imprimir(nodo.izquierda, nivel + 1, "Izq: ")
        if nodo.derecha is not None:
            self.imprimir(nodo.derecha, nivel + 1, "Der: ")

# Demostración
treap = Treap()
treap.insertar(3)
treap.insertar(1)
treap.insertar(4)
treap.insertar(2)

treap.imprimir()
