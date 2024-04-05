# Entrar desde la terminal a la carpeta 
# python3 -m manim -pql LineSegmentIntersection.py main Animation
import numpy as np
import bisect
import random
from manim import *
import heapq
from BasicAnim import Basic_Animations
import Order_orientation as Oo


# Los eventos de la priority queue
class Event:
    def __init__(self, y, x, segments, event_type, i):
        self.y =  y
        self.x =  x
        self.segments = segments # Segmentos en el que se encuentra el punto, si es un evento interseccion pueden ser multiples
        self.event_type = event_type  # 'start', 'end' o 'intersection'
        self.i = i # El indice de punto que es en el arreglo points

    def __lt__(self, other):
        # Orden
        return self.y > other.y if self.y != other.y else self.x < other.x

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
        heapq.heappush(pq_events, new_event)

    return pq_events

# La siguiente funcion detecta si hay una interseccion despues de los movimientos nuevos en el SweepLine
'''
def Detecta_intersecciones(pq_events, SweepLine):
    # Detectamos intersecciones
    intersecciones = []

    # Si hubo intersecciones las agregamos como evento
    while intersecciones:
        new_event = Event(p[1], p[0], [s], 'start', i)
        heapq.heappush(pq_events, new_event)
'''


class Animation(Basic_Animations):
    def construct(self):
        # In this function you do all the functions used for the final animation
        n = 8
        segments, points = self.random_lines(n)
        # Inicializamos los eventos 
        pq_events = create_events(points) 
        # Para 
        SweepLine = [] # Linea de barrido 

        while pq_events: # Mientras tengamos eventos
            event = heapq.heappop(pq_events)
            self.color_point(points[event.i], "BLUE")

            if event.event_type == 'start':
                # Agregamos el segmento a la linea de barrido
                s = event.segments[0]
                heapq.heappush(SweepLine, s)

                # Vemos si hay nuevas intersecciones


                # Pintamos de rojo los segmentos que estan en la linea de barrido
                p1 = points[s*2]
                p2 = points[s*2+1]
                self.color_line_from_points(p1, p2, "RED")
            
            if event.event_type == 'end':
                # Quitamos el segmento de la linea de barrido
                s = event.segments[0]

                # Vemos si hay nuevas intersecciones

                # Quitamos el rojo de los segmentos que ya no estan en la linea de barrido
                p1 = points[s*2]
                p2 = points[s*2+1]
                self.color_line_from_points(p1, p2, "WHITE")


        #for i in range(n):
        #    for j in range(i, n):
        #        self.intersect_twolines(points, i, j)
        self.wait(4)

if __name__ == "__main__":
    scene = Animation()
    scene.render()
