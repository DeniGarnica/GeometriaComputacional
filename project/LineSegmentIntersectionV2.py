# Entrar desde la terminal a la carpeta 
# python3 -m manim -pql LineSegmentIntersection.py main Animation
import numpy as np
import bisect
import random
from manim import *
import heapq
from BasicAnim import Basic_Animations
import Order_orientation as Oo
from Treap import Nodo, Treap_segments


# Los eventos de la priority queue
class Event: 
    def __init__(self, y, x, segments, event_type, i):
        self.y =  y
        self.x =  x
        self.segments = segments # Segmentos en el que se encuentra el punto, si es un evento interseccion pueden ser multiples
        self.event_type = event_type  # 'start', 'end' o 'intersection'
        self.i = i # El indice de punto que es en el arreglo points # Si es -1, no esta ahi

    '''def __lt__(self, other):
        # Orden
        return self.y > other.y if self.y != other.y else self.x < other.x'''

def create_events(points):
    pq_events = [] # Cola de prioridad de eventos

    # ordenamos los puntos por eje y para iniciar la cola de prioridad
    order = Oo.order_points_y(points)

    # Agregamos los eventos dependiendo si es el inicio o fin de un segmento
    # El segmento i
    for i in order:
        if i % 2 == 0: # Es upper
            p = points[i].get_center()
            q = points[i+1].get_center()
            s = int(i/2)
            new_event = Event(p[1], p[0], [s], 'start', i)
        else: # Es lower
            p = points[i-1].get_center()
            q = points[i].get_center()
            s = int(i/2)
            new_event = Event(q[1], q[0], [s], 'end', i)
        pq_events
        heapq.heappush(pq_events, (-new_event.y, new_event))

    return pq_events


def add_checked_pair(checked_segments, seg1, seg2):
    # Ordenar los segmentos para garantizar que el par sea consistente
    ordered_pair = tuple(sorted((seg1, seg2)))
    checked_segments.add(ordered_pair)

# Función para verificar si un par de segmentos ya ha sido revisado
def is_checked(checked_segments, seg1, seg2):
    ordered_pair = tuple(sorted((seg1, seg2)))
    return ordered_pair in checked_segments

# La siguiente funcion detecta si hay una interseccion despues de los movimientos nuevos 
# en el SweepLine
# Se le pasa la clave del que acabamos de agregar, la linea de barrido, la cola de prioriedad 
# y donde estamos almacenando las intersecciones
def Detecta_intersecciones(seg, SweepLine, pq_events, intersections, anim, checked_segments, do_izq = 1, do_der = 1):
    n = SweepLine.nodos_por_clave[seg]
    izq, der = SweepLine.izq_der(seg) 
    b = 0
    p = None
    if izq and do_izq:
        b, p = Oo.intersect_twolines(izq.p1, izq.p2, n.p1, n.p2)
        # Si hubo intersecciones las agregamos como evento
        if b:
            if not is_checked(checked_segments, izq.clave, n.clave):
                add_checked_pair(checked_segments, izq.clave, n.clave)
                print(f'se detecto intersec entre {izq.clave} y {n.clave}')
                [x,y] = p
                new_event = Event(y, x, [izq.clave, seg], 'intersecction', -1)
                heapq.heappush(pq_events, (-new_event.y, new_event))

                intersections.append([x,y])

                anim.wait(0.5)
                dot1 = Dot(point=np.array([x, y, 0]))
                anim.add(dot1)
                dot1.set_color("White")
                anim.wait(0.5)


    if der and do_der:
        b, p = Oo.intersect_twolines(der.p1, der.p2, n.p1, n.p2)
        # Si hubo intersecciones las agregamos como evento
        if b:
            if not is_checked(checked_segments, der.clave, n.clave):
                add_checked_pair(checked_segments, der.clave, n.clave)
                print(f'se detecto intersec entre {der.clave} y {n.clave}')
                [x,y] = p
                new_event = Event(y, x, [der.clave, seg], 'intersecction', -1)
                heapq.heappush(pq_events, (-new_event.y, new_event))
                intersections.append([x,y])

                anim.wait(0.5)
                dot1 = Dot(point=np.array([x, y, 0]))
                anim.add(dot1)
                dot1.set_color("White")
                anim.wait(0.5)



class Animation(Basic_Animations):
    def construct(self):
        # In this function you do all the functions used for the final animation
        #n = 8
        n = 8
        segments, points = self.random_lines(n)
        for p in points:
            print(p.get_center())
        # Inicializamos los eventos, que son los inicios y fin de segmentos
        pq_events = create_events(points) 
        for p in pq_events:
            print(p[1].segments)
        SweepLine = Treap_segments() # Linea de barrido 
        intersections = []
        checked_segments = set()

        while pq_events: # Mientras tengamos eventos
            event = heapq.heappop(pq_events)[1]
            print("event", event.segments[0], ",", event.event_type)
            '''for p in pq_events:
                print(p[0],", ", p[1].segments)'''
            # Mantendremos pintados de azul los puntos que ya procesamos
            self.color_point(points[event.i], "BLUE")

            if event.event_type == 'start':
                # Agregamos el segmento a la linea de barrido
                s = event.segments[0] # Esta es la clave del segmento 
                p1 = points[s*2] # El inicio de segmento
                p2 = points[s*2+1] # El fin de segmento
                SweepLine.insertar(s, p1, p2)
                SweepLine.imprimir()

                # Pintamos de rojo los segmentos que estan en la linea de barrido
                self.color_line_from_points(p1, p2, "RED")

                # Vemos si hay nuevas intersecciones
                Detecta_intersecciones(s, SweepLine, pq_events, intersections, self, checked_segments)

            
            if event.event_type == 'end':
                # Quitamos el segmento de la linea de barrido
                s = event.segments[0]
                p1 = points[s*2]
                p2 = points[s*2+1]

                izq = None
                der =  None

                if len(SweepLine.nodos_por_clave) > 0:
                    izq, der = SweepLine.izq_der(s)
                SweepLine.eliminar(s)

                # Vemos si hay nuevas intersecciones
                if izq and der:
                    b, p = Oo.intersect_twolines(izq.p1, izq.p2, der.p1, der.p2)
                    print(b, p)
                    if b:
                        if not is_checked(checked_segments, izq.clave, der.clave):
                            print(f'se detecto intersec entre {izq.clave} y {der.clave}')
                            add_checked_pair(checked_segments, izq.clave, der.clave)
                            x = p.get_center()[0]
                            y = p.get_center()[1]
                            new_event = Event(y, x, [izq.clave, der.clave], 'intersecction', -1)
                            heapq.heappush(pq_events, (-new_event.y, new_event))
                            intersections.append([x,y])

                            self.wait(0.5)
                            dot1 = Dot(point=np.array([x, y, 0]))
                            self.add(dot1)
                            dot1.set_color("White")
                            self.wait(0.5)

                # Quitamos el rojo de los segmentos que ya no estan en la linea de barrido
                self.color_line_from_points(p1, p2, "WHITE") 
            if event.event_type == 'intersecction':
                print(f'{event.segments[0]} inter {event.segments[1]}')
                # Marcamos la interseccion
                x = event.x
                y = event.y
                print("nodos, clave")
                print(SweepLine.nodos_por_clave)
                dot1 = Dot(point=np.array([x, y, 0]))
                self.add(dot1)
                dot1.set_color("BLUE") 
                self.wait(0.5)
                nodo1 = SweepLine.nodos_por_clave[event.segments[0]]
                nodo2 = SweepLine.nodos_por_clave[event.segments[1]]

                # Vemos cual era el de izquierda y el de dercha
                side = Oo.which_side(nodo1.p1, nodo1.p2, nodo2.p1)

                # Hacemos swap de los correspondientes
                SweepLine.swap(event.segments[0], event.segments[1])

                # Checamos intersecciones correspondientes
                if side != 1: # El segundo estaba a la izquierda
                    #print("a")
                    Detecta_intersecciones(event.segments[0], SweepLine, pq_events, intersections, self, checked_segments, do_der=0)
                    Detecta_intersecciones(event.segments[1], SweepLine, pq_events, intersections, self, checked_segments, do_izq=0)
                else: 
                    #print("b")
                    Detecta_intersecciones(event.segments[0], SweepLine, pq_events, intersections, self, checked_segments, do_izq=0)
                    Detecta_intersecciones(event.segments[1], SweepLine, pq_events, intersections, self, checked_segments, do_der=0)


            #SweepLine.imprimir()
            if len(SweepLine.nodos_por_clave) > 0:
                SweepLine.imprimir()


        #for i in range(n):
        #    for j in range(i, n):
        #        self.intersect_twolines(points, i, j)
        self.wait(4)

if __name__ == "__main__":
    scene = Animation()
    scene.render()
