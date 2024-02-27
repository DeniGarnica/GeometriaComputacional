# Entrar desde la terminal a la carpeta 
# python3 -m manim -pql LineSegmentIntersection.py main Animation
import numpy as np
from manim import *


def order(p):
    return p[0], p[1]
    
def vec_2points(p1, p2):
    return (p2[0] - p1[0], p2[1] - p1[1])

def cross_product(vec1, vec2):
    return vec1[0] * vec2[1] - vec1[1] * vec2[0]

def lineDist(p1, p2, p):
    return abs((p[1] - p1[1]) * (p2[0] - p1[0]) -
            (p2[1] - p1[1]) * (p[0] - p1[0]))


class Basic_Animations(Scene):
    def construct_randpoints(self, n = 20):
        points = []
        x = 4
        y = 3
        self.wait(1)
        for i in range(n):
            x_r = np.random.uniform(-x, x)
            y_r = np.random.uniform(-y, y)
            points.append(Dot(point=np.array([x_r, y_r, 0])))
        group = VGroup(*points)
        self.play(Create(group, run_time=6.0))
        self.wait(1)
        return points
    
    def join_points(self, p1, p2):
        line = Line(p1, p2)
        self.play(Create(line, run_time=1.0))
        self.wait(1)
        return line

    def color_point(self, point, color):
        point.set_color(color)
        self.wait(0.5)
    
    def color_line(self, line, color):
        line.set_color(color)
        self.wait(0.1)

    def highlight_line(self, line, color):
        line.set_color(color)
        self.wait(2)
        line.set_color("WHITE")
        self.wait(1)
    
    def highlight_point(self, point, color):
        point.set_color(color)
        self.wait(1)
        point.set_color("WHITE")
        self.wait(1)
    
    def order_points(self, points):
        #returns an array of the order of the points, not the array ordered
        return sorted(range(len(points)), key=lambda i: order(points[i].get_center()))
    
    # Ve de que lado esta el punto p, respecto a la recta formada por p1, p2
    def which_side(self, p1, p2, p):
        vec1 = vec_2points(p1.get_center(), p2.get_center())
        vec2 = vec_2points(p1.get_center(), p.get_center())
        cross_p = cross_product(vec1, vec2)
        if cross_p > 0:
            return 1 # Right
        elif cross_p < 0:
            return -1 # Left
        else: 
            return 0 # On the line

    # Devuelve indices de los puntos que pertenecen a la izqueirda y derecha de la linea
    # formada por p1 y p2
    def div_sides(self, p1, p2, points):
        left = []
        right = []
        for i in range(len(points)):
            side = self.which_side(p1, p2, points[i])
            if  side == 1:
                left.append(i)
            if  side == -1:
                right.append(i)
        return left, right

    # Side es el cnojunto de indices de puntos que estan en cierto lado de la recta
    # formada por p1 y p2
    def lejano(self, p1, p2, points, side):
        max_d = 0.0
        ind = -1
        for i in range(len(side)):
            l_d = lineDist(p1.get_center(), p2.get_center(), points[side[i]].get_center())
            if l_d > max_d:
                max_d = l_d
                ind = side[i]
        return ind
    
    def subset(self, points, side):
        sub = []
        for i in range(len(side)):
            sub.append(points[side[i]])
        return sub

    def add_to_ch(self, c_h, p1, p2, p):
        # Encuentra los índices de los elementos en la lista
        ind1 = -1
        ind2 = -1
        if p1 in c_h:
            ind1 = c_h.index(p1)
        if p2 in c_h:
            ind2 = c_h.index(p2)
        
        if ind1 == -1:
            if ind2 == len(c_h)-1:
                c_h.append(p)
            else:
                c_h.insert(0, p)
            return c_h

        if ind2 == -1:
            if ind2 == len(c_h)-1:
                c_h.append(p)
            else:
                c_h.insert(0, p)
            return c_h

        if ind2 > ind1:
            c_h.insert(ind1+1, p)
        else:
            c_h.insert(ind2+1, p)

        return c_h

    def random_lines(self, n = 10):
        points = self.construct_randpoints(2*n)
        lines = []
        i = 0
        for j in range(n):
            lines.append(self.join_points(points[i], points[i+1]))
            i = i + 2
        return lines, points

    def intersect_twolines(self, lines, points, i, j):
        # Los 4 puntos que conforman a los dos segmentos de recta
        p1 = points[2*i]
        p2 = points[2*i + 1]
        p3 = points[2*j]
        p4 = points[2*j + 1]

        # Vemos de que lado estan los puntos respecto al otro segmento de recta
        # Si alguno es 0 significa que esta en la linea
        s1 = self.which_side(p1, p2, p3)
        if s1 == 0:
            return 1, p3
        s2 = self.which_side(p1, p2, p4)
        if s2 == 0:
            return 1, p4
        s3 = self.which_side(p3, p4, p1)
        if s3 == 0:
            return 1, p1
        s4 = self.which_side(p3, p4, p2)
        if s4 == 0:
            return 1, p2

        # Si estan del mismo lado significa que no se cruzan
        if s1 == s2:
            return 0, None
        if s3 == s4:
            return 0, None

        # Calcular las pendientes
        p1 = p1.get_center()
        p2 = p2.get_center()
        p3 = p3.get_center()
        p4 = p4.get_center()
        m1 = (p2[1] - p1[1]) / (p2[0] - p1[0]) if p2[0] - p1[0] != 0 else float('inf')
        m2 = (p4[1] - p3[1]) / (p4[0] - p3[0]) if p4[0] - p3[0] != 0 else float('inf')
        if m1 != float('inf') and m2 != float('inf'):
            # Calcular intercecciones de y
            b1 = p1[1] - m1 * p1[0]
            b2 = p3[1] - m2 * p3[0]

            # Calcular el punto de intersección
            x = (b2 - b1) / (m1 - m2)
            y = m1 * x + b1
        else:
            # Manejar casos donde una de las líneas es vertical
            if m1 == float('inf'):
                x = p1[0]
                y = m2 * x + (p3[1] - m2 * p3[0])
            else:
                x = p3[0]
                y = m1 * x + (p1[1] - m1 * p1[0])

        # Agregamos el punto a la animacion en caso de que cruce
        dot1 = Dot(point=np.array([x, y, 0]))
        self.add(dot1)
        dot1.set_color("RED")
        self.wait(0.5)

        # Al ser diferentes se curzan y debemos ver en donde
        return 1, [x, y]

class Animation(Basic_Animations):
    def construct(self):
        # In this function you do all the functions used for the final animation
        n = 8
        lines, points = self.random_lines(n)

        for i in range(n):
            for j in range(i, n):
                self.intersect_twolines(lines, points, i, j)

if __name__ == "__main__":
    scene = Animation()
    scene.render()
