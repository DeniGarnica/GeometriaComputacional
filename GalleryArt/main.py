# python3 -m manim -pql main.py main Animation  


import Poligon as Poly
import numpy as np
import bisect
import random
from manim import *
import heapq
from BasicAnim import Basic_Animations
import Order_orientation as Oo
from Poligon import Edge
import copy
from collections import Counter

def polig_ejemp():
    points = []

    s = 1.1
    x = -1.5
    points.append(Poly.Point(s*4.1 + x, s*1.7))#1
    points.append(Poly.Point(s*3.2 + x, s*1.3))#2
    points.append(Poly.Point(s*2.7 + x, s*3.5))#3
    points.append(Poly.Point(s*2 + x, s*3))#4
    points.append(Poly.Point(s*1.5 + x, s*3.2))#5
    points.append(Poly.Point(s*0.7 + x, s*2.5)) #6
    points.append(Poly.Point(s*1.2 + x, s*1.9)) #7
    points.append(Poly.Point(s*1 + x, s*1)) # 8
    points.append(Poly.Point(s*0.5 + x, s*1.4)) #9
    points.append(Poly.Point(s*0 + x, s*0)) #10
    points.append(Poly.Point(s*0.9 + x, s*-1.7))#11
    points.append(Poly.Point(s*1.7 + x, s*-1.3))#12
    points.append(Poly.Point(s*2.8 + x, s*-2.2))#13
    points.append(Poly.Point(s*2.7 + x, s*-0.3))#14
    points.append(Poly.Point(s*3.9 + x, s*-1))#15
    

    Poligono = Poly.Polygon(points)

    return Poligono

def split_list_by_elements(lst, v1, v2):
    # Encuentra los índices de v1 y v2
    try:
        index1 = lst.index(v1)
        index2 = lst.index(v2)
    except ValueError:
        # Uno de los elementos no está en la lista
        return None
    # Asegúrate de que index1 es menor que index2
    if index1 > index2:
        index1, index2 = index2, index1  # Intercambia si v2 viene antes de v1

    # Divide la lista
    part1 = lst[:index1+1]  # Todo antes de v1
    part2 = lst[index1+1:index2]  # Desde v1 a v2, exclusivo
    part3 = lst[index2:]  # Todo después de v2

    return part1, part3, part2

def split_list_by_elements_inc(lst, v1, v2):
    # Encuentra los índices de v1 y v2
    try: 
        index1 = lst.index(v1)
        index2 = lst.index(v2)
    except ValueError:
        # Uno de los elementos no está en la lista
        return None
    # Asegúrate de que index1 es menor que index2
    if index1 > index2:
        index1, index2 = index2, index1  # Intercambia si v2 viene antes de v1

    # Divide la lista, aqui ERROR
    part1 = lst[:index1]  # Todo antes de v1
    part2 = lst[index1:index2+1]  # Desde v1 a v2, inclusive
    part3 = lst[index2+1:]  # Todo después de v2

    return part1, part3, part2

def adds_edge(Poly, v1, v2, anim):
    points = Poly.vertices
    edges = Poly.edges

    new_Poly = copy.copy(Poly)
    v1_c = copy.deepcopy(v1)
    v2_c = copy.deepcopy(v2)
    #anim.color_edge(v1_c.edge, "RED")
    #anim.color_edge(v2_c.edge, "PINK")

    # Dividimos los puntos
    # En p1 se mantienen los orginales
    points_p1, points_p3, points_2 = split_list_by_elements(points, v1, v2)


    # Juntamos las dos partes que quedaron separadas
    points_2.append(v1_c)
    points_2.append(v2_c)
    points_1 = points_p1 + points_p3

    Poly.vertices = points_1
    new_Poly.vertices = points_2

    # Modificamos quien esta a la izquierda y derecha de quien
    v1_c.izq = v2_c
    v1_c.der = v1.der
    v1_c.der.izq = v1_c

    v2_c.der = v1_c
    v2_c.izq = v2.izq
    v2_c.izq.der = v2_c
    

    #anim.color_edge(v1.edge.prev, "RED")
    #anim.color_edge(v1.edge, "YELLOW")

    edges_p1, edges_p3, edges_2  = split_list_by_elements(edges, v2.edge.prev, v1.edge)
    # Creamos la nueva arista
    new_edge = Edge(v1, v2) 
    new_edge_c = Edge(v1_c, v2_c)

     # Juntamos las partes separadas
    edges_p1.append(new_edge)
    edges_1 = edges_p1 + edges_p3
    Poly.edges = edges_1

    edges_2.append(new_edge_c)
    
    # Modificamos quien esta a la prev y next de quien
    v2_c.edge.next.prev = v2_c
    v2_c.edge.prev.next = v2_c
    v1_c.edge.next.prev = v1_c
    v1_c.edge.prev.next = v1_c
    if edges_2[0] == v2.edge:
        edges_2[0] = v2_c.edge
        edges_2[0].next = v2_c.edge.next
        edges_2[0].prev = v2_c.edge.prev
        edges_2[0].next.next = new_edge_c

    new_edge_c.next = v2_c.edge
    v2_c.edge.prev = new_edge_c
    new_edge_c.prev = v1_c.edge.prev
    v1_c.edge.prev.next = new_edge_c
    v1_c.edge = new_edge_c 

    new_Poly.edges = edges_2


    new_edge.prev = v2.edge.prev
    v2.edge.prev.next = new_edge
    new_edge.next = v1.edge
    new_edge.next.prev = new_edge
    v2.edge = new_edge

    v2.izq = v1
    v1.der = v2
    
    #new_Poly.mark_poli(anim, "ORANGE")

    return Poly, new_Poly

def adds_edge_v2(Poly, v1, v2, anim):
    #anim.color_point(v1, "RED")
    #anim.color_point(v2, "PINK")
    #anim.color_edge(v1.edge, "RED")
    points = Poly.vertices
    edges = Poly.edges

    new_Poly = copy.copy(Poly)
    v1_c = copy.deepcopy(v1)
    v2_c = copy.deepcopy(v2)
    #anim.color_point(v1_c, "RED")
    #anim.color_point(v2_c, "PINK")

    # Dividimos los puntos
    # En p2 se mantienen los orginales
    points_p1, points_p3, points_2 = split_list_by_elements_inc(points, v2, v1)

    # Juntamos las dos partes que quedaron separadas
    points_p1.append(v2_c)
    points_p1.append(v1_c)
    points_1 = points_p1 + points_p3 

    new_Poly.vertices = points_1
    Poly.vertices = points_2

    # Modificamos quien esta a la izquierda y derecha de quien
    v1_c.der = v2_c
    v1_c.izq = v1.izq
    v1_c.izq.der = v1_c

    v2_c.izq = v1_c
    v2_c.der = v2.der
    v2_c.der.izq = v2_c



    edges_p1, edges_p3, edges_2  = split_list_by_elements_inc(edges, v2.edge, v1.edge.prev)
    # Creamos la nueva arista
    new_edge = Edge(v1, v2) 
    new_edge_c = Edge(v1_c, v2_c)

    # Juntamos las partes separadas
    edges_p1.append(new_edge_c)
    edges_1 = edges_p1 + edges_p3
    new_Poly.edges = edges_1

    # El original se queda en Poly
    edges_2.append(new_edge)
    Poly.edges = edges_2



    # Modificamos quien esta a la prev y next de quien
    new_edge_c.next = v1_c.edge
    new_edge_c.next.prev = new_edge_c 

    new_edge_c.prev = v2_c.edge.prev
    new_edge_c.prev.next = new_edge_c 
    #anim.color_edge(new_edge_c.prev, "BLUE")
    #anim.color_edge(new_edge_c.prev.next, "RED")

    v2_c.edge = new_edge_c
    
    #anim.color_edge(v2_c.edge.prev, "BLUE")
    #anim.color_edge(v2_c.edge.prev.next, "RED")
    

    v2.der = v1
    v1.izq = v2

    new_edge.next = v2.edge
    new_edge.next.prev = new_edge

    new_edge.prev = v1.edge.prev
    new_edge.prev.next = new_edge
    v2.edge = new_edge
    
    v1.edge = new_edge 
    #new_Poly.mark_points(anim, "BLUE")
    

    return Poly, new_Poly

def split_polygon_to_monotones(polygon, anim):
    Poligons = []
    vertices_sorted = sorted(polygon.vertices, key=lambda v: (v.y, v.x), reverse=True)
    active_edges = Poly.ActiveEdgeList()

    # la arista izquierda de un punto es nombrada con ese mismo punto

    for i, vertex in enumerate(vertices_sorted):
        #print(f'{i}: {vertex}. {vertex.izq}')
        if vertex.type == 'start':
            print('start')
            active_edges.add(vertex)
            vertex.helper = vertex   

        if vertex.type == 'end':
            print('end')
            v_p = vertex
            print(f'{v_p}, v_p')
            if v_p.helper and v_p.helper.type == 'merge':
                polygon, new_Poly = adds_edge(polygon, vertex, v_p.helper, anim)
                #new_Poly.mark_poli(anim) 
                #new_Poly.mark_points(anim) 
                Poligons.append(new_Poly)
                anim.join_points(vertex, v_p.helper) 

            active_edges.remove(v_p)
        
        
        if vertex.type == 'split':
            print('split')
            left = active_edges.find_left(vertex)

            if left:
                print(f"Connecting {vertex} to helper of {left}")
                if left.helper.type == 'merge':
                    anim.join_points(vertex, left.helper)
                    polygon, new_Poly = adds_edge_v2(polygon, vertex, left.helper, anim)
                    #new_Poly.mark_points(anim) 
                    #new_Poly.mark_poli(anim) 
                    Poligons.append(new_Poly)
                    left.helper = vertex
                    print(f'v: {vertex}, v.der: {vertex.der}')
                    active_edges.add(vertex.der)
                    vertex.helper = vertex
                else:
                    anim.join_points(vertex, left.helper)
                    polygon, new_Poly = adds_edge(polygon, left.helper, vertex, anim)
                    #new_Poly.mark_points(anim) 
                    #new_Poly.mark_poli(anim) 
                    Poligons.append(new_Poly)
                    left.helper = vertex
                    print(f'v: {vertex}, v.der: {vertex.der}')
                    active_edges.add(vertex.der)
                    vertex.helper = vertex


        if vertex.type == 'merge':
            print('merge')
            v_p = vertex.der
            if v_p.helper and v_p.helper.type == 'merge':
                anim.join_points(vertex, v_p.helper)
                polygon, new_Poly = adds_edge(polygon, vertex, v_p.helper, anim)
                #new_Poly.mark_points(anim) 
                #new_Poly.mark_poli(anim) 
                Poligons.append(new_Poly)
            active_edges.remove(v_p)
            left = active_edges.find_left(vertex)
            print(f'left de {vertex} es {left}')
            if left:
                if left.helper and left.helper.type == 'merge':
                    anim.join_points(vertex, left.helper)
                    polygon, new_Poly = adds_edge(polygon, vertex, left.helper, anim)
                    #new_Poly.mark_points(anim) 
                    #new_Poly.mark_poli(anim) 
                    Poligons.append(new_Poly)
                left.helper = vertex

        if vertex.type == '':
            print('n') 
            side = -1 # Ver si esta a la izquierda o derecha del poligono
            if side == -1: # el resto del polig esta a la derecha
                #print('int der')
                v_p = vertex.der # el de arriba
                if v_p: 
                    if v_p.helper and v_p.helper.type == 'merge':
                        anim.join_points(vertex, v_p.helper)
                        polygon, new_Poly = adds_edge(polygon, vertex, v_p.helper, anim)
                        #new_Poly.mark_points(anim) 
                        Poligons.append(new_Poly)
                        #new_Poly.mark_poli(anim) 
                        active_edges.remove(v_p)
                    active_edges.add(vertex)
                    vertex.helper = vertex
            else:
                left = active_edges.find_left(vertex)
                if left: 
                    if left.helper.type == 'merge':
                        #print(f'left de {vertex} es {left}')
                        anim.join_points(vertex, left.helper)
                        polygon, new_Poly = adds_edge(polygon, vertex, left.helper, anim)
                        #new_Poly.mark_points(anim) 
                        #new_Poly.mark_poli(anim) 
                        Poligons.append(new_Poly)
                    left.helper = vertex
                    print(f'left de {vertex} es {left}')
    Poligons.append(polygon)
    #polygon.mark_poli(anim)
    return Poligons

def monotone_to_triangles(polygon, anim, n):
    #polygon.mark_points(anim)
    triangles = []
    ver = polygon.vertices
    if len(polygon.vertices) == 3:
        t = [ver[0], ver[1], ver[2]]
        
        triangles.append(t)
        return triangles
    
    polygon.sort_vertices()
    cola = []
    for i, v in enumerate(polygon.vertices):
        color = 0
        if i == 0:
            ref = v
            prev = v
            v.color = color
            color+=1
            continue
        if v == ref.izq or v == ref.der:
            cola.append(v)
            v.color = color%3
            color += 1
            ref = v
        else:
            for c in cola:
                anim.join_points(v, c) 
                t = [v, c, prev]
                triangles.append(t)
                prev = c
            cola = [v]
            ref = v
    if len(cola) != 0:
        for i, c in enumerate(cola):
            anim.join_points(ref, c)
            if i != len(cola)-1:
                t = [v, c, prev]
                prev = c
                triangles.append(t)
        
    return triangles

def are_adjacent(tri1, tri2):
    set1 = { (p.x, p.y) for p in tri1 }
    set2 = { (p.x, p.y) for p in tri2 }
    return len(set1 & set2) == 2

class Animation(Basic_Animations):

    def color_type(self, p):
        if p.type == 'end':
            self.color_point(p, '#43b8f7') # Azul
        if p.type == 'start':
            self.color_point(p, '#f7d043') # amarillo
        if p.type == 'split':
            self.color_point(p, 'PURPLE')
        if p.type == 'merge':
            self.color_point(p, '#519660') # Verde
        if p.type == '':
            self.color_point(p, 'WHITE')


    def construct(self):
        Poligono = polig_ejemp()
        vertex = Poligono.vertices
        for i in range(len(vertex)-1):
            self.join_points(vertex[i], vertex[i+1])
            self.color_type(vertex[i])
        self.join_points(vertex[-1], vertex[0]) 
        self.color_type(vertex[-1])

        # Monotonizamos nuestro poligono
        Poligons = split_polygon_to_monotones(Poligono, self)
        triangles = []

        # Triangulamos los poligonos monotonos
        #for poly in Poligons:
        n = 0
        for poly in Poligons:
            n_triangles = monotone_to_triangles(poly, self, n)
            triangles.append(n_triangles)
            n += 1
        triangles = [element for sublist in triangles for element in sublist]

        print(triangles)

        graph = {i: set() for i in range(len(triangles))}
        for i in range(len(triangles)):

            for j in range(i + 1, len(triangles)):
                if are_adjacent(triangles[i], triangles[j]):
                    graph[i].add(j)
                    graph[j].add(i)



        v1, v2, v3 = triangles[0]
        vertex = {}
        vertex[(v1.x, v1.y)] = 0
        vertex[(v2.x, v2.y)] = 1
        i = 0

        # DFS de los triangulos
        visited = set()
        stack = [0]
        while stack:
            actual = stack.pop()
            if actual not in visited:
               # coloreamos suponiendo que dos vertices ya estan coloreados
                coloreados = []
                no_esta = None
                for punto in triangles[actual]: # Vemos los 3 puntos
                    if (punto.x, punto.y) in vertex: # Para ver que dos colores ya se usaron
                        coloreados.append(vertex[(punto.x, punto.y)])
                    else: # Vemos cual no esta coloreado
                        no_esta = punto
                # Vemos que color falta
                n_color = next(valor for valor in [0, 1, 2] if valor not in coloreados)
                # Coloreamos
                vertex[(no_esta.x, no_esta.y)] = n_color

                visited.add(actual)

                # Vemos los vecinos
                for neigh in graph[actual]:
                    if neigh not in visited:
                        stack.append(neigh)

        # Coloreamos los vertices de los triangulos
        for v, color in vertex.items():
            if color == 0:
                color = "GREEN"
            if color == 1:
                color = "PURPLE"
            if color == 2:
                color = "WHITE"
            self.color_point_tupla(v, color)

        # Elejimos donde poner los guardias
        conteos = Counter(vertex.values())
        menor_valor = min(conteos, key=conteos.get)
        menor_conteo = conteos[menor_valor]
        if menor_valor == 0:
                color = "GREEN"
        if menor_valor  == 1:
            color = "PURPLE"
        if menor_valor == 2:
            color = "WHITE"

        print(f'Se necesitan al menos {menor_conteo} guardias en los puntos {color}')

        for v, color in vertex.items():
            if color == 0:
                self.color_point_tupla(v, "RED")

        self.wait(5)


if __name__ == "__main__":
    scene = Animation()
    scene.render()