import Order_orientation as Oo
import bisect
from sortedcontainers import SortedList

class Point:
    def __init__(self, x, y): 
        self.x = x
        self.y = y 
        # En sentido antihorario
        self.izq = None
        self.der = None
        self.type = '' 
        self.helper = None
        # Cada punto apunta a su edge en sentido antihorario
        self.edge = None
        self.color = None

    '''def __lt__(self, other):
        return (self.y, self.x) > (other.y, other.x) if isinstance(other, Point) else NotImplemented'''
    def __lt__(self, other):
        return self.x < other.x if isinstance(other, Point) else NotImplemented

    def __repr__(self):
        return f"({self.x}, {self.y})"
    
class Edge:
    def __init__(self, p1, p2):
        if p1.y >= p2.y:
            self.p1 = p1
            self.p2 = p2
        else:
            self.p1 = p2
            self.p2 = p1
        self.next = None
        self.prev = None

class Polygon:
    def __init__(self, points):
        self.vertices = points

        # Creamos el orden de los puntos asuminedo que en points nos los dieron en orden
        points[0].der = points[-1]
        points[-1].izq = points[0]
        n_edge = Edge(points[0], points[-1])
        points[-1].edge = n_edge


        for i in range(len(points)-1):
            points[i].izq = points[i+1]
            points[i+1].der = points[i]
            n_edge = Edge(points[i], points[i+1])
            points[i].edge = n_edge
            #points[i+1].edge = n_edge
        self.find_type() 
        self.edges = self.process_edges(points)

    def __repr__(self):
        return f"(Este poligono tiene {len(self.vertices)} vertices y  {len(self.edges)} aristas.)"
    
    def sort_vertices(self):
        # Ordena los vértices por y de mayor a menor
        self.vertices.sort(key=lambda point: point.y, reverse=True)

    def type(self, v0,v1,v2):
        side = Oo.which_side(v0, v2, v1)
        if side == -1: # Esta a la derecha
            if v0.y < v1.y and v2.y < v1.y:
                v1.type = 'start'
            if v0.y > v1.y and v2.y > v1.y:
                v1.type = 'end'
        else: # Esta a la derecha
            if v0.y < v1.y and v2.y < v1.y:
                v1.type = 'split'
            if v0.y > v1.y and v2.y > v1.y: 
                v1.type = 'merge'

    def find_type(self):
        points = self.vertices

        for i in range(len(points)-1):
            v0 = points[i-1]
            v1 = points[i]
            v2 = points[i+1]

            self.type(v0,v1,v2)

        v0 = points[len(points)-2]
        v1 = points[-1]
        v2 = points[0]
        self.type(v0,v1,v2)

    def process_edges(self, points):
        edges = []
        for p in points:
            edge = p.edge
            edge.next = p.izq.edge
            edge.prev = p.der.edge
            edges.append(edge)

        return edges 

    def mark_poli(self, anim, color = 'PURPLE'):
        edges = self.edges
        ed = edges[0]
        for i in range(len(edges)):
            anim.color_edge(ed, color)
            ed = ed.next

    def mark_points(self, anim, color = 'RED'):
        points = self.vertices
        p = points[0]
        for i in range(len(points)):
            anim.color_point(p, color)
            p = p.der


class ActiveEdgeList:
    def __init__(self):
        self.edges = SortedList()

    def add(self, vertex):
        self.edges.add(vertex)

    def remove(self, vertex):
        self.edges.discard(vertex) 

    def get_all_edges(self):
        return list(self.edges)
    
    def it_edge(self, i):
        if len(self.edges) > i:  # Verifica que la lista no esté vacía
            return self.edges[i]
        return None  # Retorna None si la lista está vacía

    def find_left(self, vertex):
        pos = self.edges.bisect_left(vertex) - 1
        if pos >= 0:
            return self.edges[pos]
        return None
    
    def find_right(self, vertex):
        pos = self.edges.bisect_right(vertex) - 1
        if pos >= 0:
            return self.edges[pos]
        return None

