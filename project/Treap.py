import random
import Order_orientation as Oo

class Nodo:
    def __init__(self, clave, p1, p2, prioridad=None):
        self.clave = clave # El nombre del segmento
        self.p1 = p1 # El punto que marca el inicio del segmento
        self.p2 = p2 # El punto que marca el fin del segmento
        self.prioridad = prioridad if prioridad is not None else random.random() # Para que se autobalancen
        self.izquierda = None
        self.derecha = None

class Treap_segments:
    def __init__(self):
        self.raiz = None

    def insertar(self, clave, p1, p2, prioridad=None):
        if not self.raiz:
            self.raiz = Nodo(clave, p1, p2, prioridad)
        else:
            self.raiz = self._insertar(self.raiz, clave, p1, p2, prioridad)

    def _insertar(self, nodo, clave, p1, p2, prioridad):
        if not nodo:
            return Nodo(clave, p1, p2, prioridad)

        position = Oo.which_side(nodo.p1, nodo.p2, p1)
        if  position == -1: # Si el inicio del segmento esta a la izq 
            nodo.izquierda = self._insertar(nodo.izquierda, clave, p1, p2, prioridad)
            if nodo.izquierda.prioridad > nodo.prioridad:
                nodo = self.rotar_derecha(nodo)
        elif position == 1: # Si el inicio del segmento esta a la der
            nodo.derecha = self._insertar(nodo.derecha, clave, p1, p2, prioridad)
            if nodo.derecha.prioridad > nodo.prioridad:
                nodo = self.rotar_izquierda(nodo)
        elif position == 0: # Si esta en la recta direnmos que esta a la izq
            nodo.izquierda = self._insertar(nodo.izquierda, clave, p1, p2, prioridad)
            if nodo.izquierda.prioridad > nodo.prioridad:
                nodo = self.rotar_derecha(nodo)
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

    def eliminar(self, clave, p2):
        self.raiz = self._eliminar(self.raiz, clave, p2)

    def _eliminar(self, nodo, clave, p2):
        if nodo is None:
            return None

        position = Oo.which_side(nodo.p1, nodo.p2, p2)
        if clave == nodo.clave: # Si encontramos el nodo a eliminar
            # Si es un nodo hoja, simplemente lo eliminamos
            if not nodo.izquierda and not nodo.derecha:
                return None
             # Si tiene ambos hijos, rotamos con el de mayor prioridad
            elif nodo.izquierda and nodo.derecha:
                if nodo.izquierda.prioridad > nodo.derecha.prioridad:
                    nodo = self._rotar_derecha(nodo)
                    nodo.derecha = self._eliminar(nodo.derecha, clave, p2)
                else:
                    nodo = self._rotar_izquierda(nodo)
                    nodo.izquierda = self._eliminar(nodo.izquierda, clave, p2)
            # Si solo tiene un hijo, lo rotamos hacia arriba
            elif nodo.izquierda:
                nodo = self._rotar_derecha(nodo)
                nodo.derecha = self._eliminar(nodo.derecha, clave, p2)
            else:  # Solo tiene hijo derecho
                nodo = self._rotar_izquierda(nodo)
                nodo.izquierda = self._eliminar(nodo.izquierda, clave, p2)
        elif position != 1: # Si esta en el segmento o a la izquierda
            nodo.izquierda = self._eliminar(nodo.izquierda, clave, p2)
        else: # Si esta a la derecha
            nodo.derecha = self._eliminar(nodo.derecha, clave, p2)
        
        return nodo

    # Método para imprimir el Treap (Para propósitos de depuración y visualización)
    def imprimir(self, nodo=None, nivel=0, prefijo="Raíz: "):
        if nodo is None:
            nodo = self.raiz

        print(" " * nivel * 2 + prefijo + str(nodo.clave) + " (" + str(nodo.prioridad) + ")")
        if nodo.izquierda is not None:
            self.imprimir(nodo.izquierda, nivel + 1, "Izq: ")
        if nodo.derecha is not None:
            self.imprimir(nodo.derecha, nivel + 1, "Der: ")
