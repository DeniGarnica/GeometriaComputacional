import random
import Order_orientation as Oo

class Nodo:
    def __init__(self, clave, p1, p2, prioridad=None, padre=None):
        self.clave = clave # El nombre del segmento
        self.p1 = p1 # El punto que marca el inicio del segmento
        self.p2 = p2 # El punto que marca el fin del segmento
        self.prioridad = prioridad if prioridad is not None else random.random()
        self.izquierda = None
        self.derecha = None
        self.padre = padre

class Treap_segments:
    def __init__(self):
        self.raiz = None
        self.nodos_por_clave = {}

    def insertar(self, clave, p1, p2, prioridad=None):
        if not self.raiz:
            nuevo_nodo = Nodo(clave, p1, p2, prioridad)
            self.nodos_por_clave[clave] = nuevo_nodo
            self.raiz = nuevo_nodo
        else:
            self.raiz = self._insertar(self.raiz, clave, p1, p2, prioridad)

    def _insertar(self, nodo, clave, p1, p2, prioridad):
        if not nodo:
            nuevo_nodo = Nodo(clave, p1, p2, prioridad)
            self.nodos_por_clave[clave] = nuevo_nodo
            return nuevo_nodo

        position = Oo.which_side(nodo.p1, nodo.p2, p1)
        if position != 1: # Si el inicio del segmento esta a la izq 
            nodo.izquierda = self._insertar(nodo.izquierda, clave, p1, p2, prioridad)
            nodo.izquierda.padre = nodo
            if nodo.izquierda.prioridad > nodo.prioridad:
                nodo = self.rotar_derecha(nodo)
        else: # Si el inicio del segmento esta a la der
            nodo.derecha = self._insertar(nodo.derecha, clave, p1, p2, prioridad)
            nodo.derecha.padre = nodo
            if nodo.derecha.prioridad > nodo.prioridad:
                nodo = self.rotar_izquierda(nodo)
        return nodo

    def rotar_derecha(self, y):
        x = y.izquierda
        T2 = x.derecha
        x.derecha = y
        y.izquierda = T2
        x.padre = y.padre  # Actualizar el padre de x
        y.padre = x  # El nuevo padre de y es x
        if T2: T2.padre = y  # Actualizar el padre de T2, si existe
        return x

    def rotar_izquierda(self, x):
        y = x.derecha
        T2 = y.izquierda
        y.izquierda = x
        x.derecha = T2
        y.padre = x.padre  # Actualizar el padre de y
        x.padre = y  # El nuevo padre de x es y
        if T2: T2.padre = x  # Actualizar el padre de T2, si existe
        return y
    
    def eliminar(self, clave):
        if clave in self.nodos_por_clave:
            nodo_a_eliminar = self.nodos_por_clave[clave]
            self._eliminar(nodo_a_eliminar)
            if clave in self.nodos_por_clave:
                del self.nodos_por_clave[clave]  # Eliminar el nodo del diccionario
            print(self.nodos_por_clave)
        

    def _eliminar(self, nodo):
        # Eliminar un nodo con 0 o 1 hijo es directo: reemplazarlo con su hijo (si lo tiene)
        print("nclav", nodo.clave)
        if not nodo.izquierda or not nodo.derecha:
            hijo = nodo.izquierda if nodo.izquierda else nodo.derecha
            if nodo == self.raiz: # Si es la raiz
                self.raiz = hijo
                if hijo: hijo.padre = None
            elif nodo.padre.izquierda == nodo: # si es el hijo de la izquierda
                nodo.padre.izquierda = hijo
                print("1")
                if hijo: hijo.padre = nodo.padre
            else:
                nodo.padre.derecha = hijo
                if hijo: hijo.padre = nodo.padre
                print("2")
        else:
            # Checa como entender esto, para ver si la eliminacion se hace correcta
            # Tiene dos hijos, buscar el sucesor (menor nodo en el subárbol derecho)
            sucesor = self._minValueNode(nodo.derecha)
            clave_sucesor = sucesor.clave
            self._eliminar(sucesor)  # Eliminar el sucesor
            # Reemplazar el nodo a eliminar con el sucesor
            nodo.clave = sucesor.clave
            nodo.p1 = sucesor.p1
            nodo.p2 = sucesor.p2
            # Asegurarse de que el diccionario apunte al nodo actualizado
            self.nodos_por_clave[clave_sucesor] = nodo
            #del self.nodos_por_clave[sucesor.clave]

    def _minValueNode(self, nodo):
        current = nodo
        while current.izquierda is not None:
            current = current.izquierda
        return current
        

    def swap(self, clave1, clave2): 
        nodo1 = self.nodos_por_clave[clave1]
        nodo2 = self.nodos_por_clave[clave2]
        
        t_clave = nodo1.clave
        t_p1 = nodo1.p1
        t_p2 = nodo1.p2
    
        nodo1.clave = nodo2.clave
        nodo1.p1 = nodo2.p1
        nodo1.p2 = nodo2.p2

        nodo2.clave = t_clave
        nodo2.p1 = t_p1
        nodo2.p2 = t_p2

        self.nodos_por_clave[clave1] = nodo2 
        self.nodos_por_clave[clave2] = nodo1

    # nos dice si el nodo es hijo izquierdo o derecho
    def que_hijo(self, nodo): # devuelve 1 si es el hijo izquierdo, 0 si es el derecho
        if nodo == self.raiz: # Si el nodo no tiene padre
            return -1
        if nodo.padre.izquierda == nodo:
            return 1
        return 0

    # Regresa quien esta a la iquierda y dercha del nodo
    def izq_der(self, clave):
        nodo = self.nodos_por_clave[clave]
        izq = None
        der = None
        # Tiene ambos hijos o es la raiz
        if nodo == self.raiz or (nodo.izquierda and nodo.derecha):
            izq = self.mas_der(nodo.izquierda)
            der = self.mas_izq(nodo.derecha)
        # No tiene ningun hijo
        elif not nodo.izquierda and not nodo.derecha:
            if self.que_hijo(nodo) == 1: # Si es el hijo izquierdo
                der = nodo.padre
                if self.que_hijo(nodo.padre) == 0: # Si el padre fue el hijo derecho
                    izq = nodo.padre.padre
            else: # Si es el hijo derecho
                izq = nodo.padre
                if self.que_hijo(nodo.padre) == 1: # Si el padre fue el hijo izq
                    der = nodo.padre.padre
        # Tiene solo alguno de los dos hijos
        else:
            if nodo.izquierda: # Solo tiene hijo izq
                izq = self.mas_der(nodo.izquierda)
                if self.que_hijo(nodo) == 1: # Si es el hijo izq
                    der = nodo.padre
            else:
                der = self.mas_izq(nodo.derecha)
                if self.que_hijo(nodo) == 0: # Si es el hijo der
                    izq = nodo.padre
        if izq and der:
            print(f'n: {nodo.clave}, izq: {izq.clave}, der: {der.clave}')
            
        return izq, der
    # Dado un nodo nos da su sucesor mas a la derecha
    def mas_der(self, nodo):
        if not nodo:
            return None
        while nodo.derecha:
            nodo = nodo.derecha
        return nodo
    
    def mas_izq(self, nodo):
        if not nodo:
            return None
        while nodo.izquierda:
            nodo = nodo.izquierda
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
