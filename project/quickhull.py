# Entrar desde la terminal a la carpeta 
# python3 -m manim -pql quickhull.py main Animation
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
 
def which_side(p1, p2, p):
    vec1 = vec_2points(p1, p2)
    vec2 = vec_2points(p1, p)
    cross_p = cross_product(vec1, vec2)
    if cross_p > 0:
        return 1 # Right
    elif cross_p < 0:
        return -1 # Left
    else: 
        return 0 # On the line


class Basic_Animations(Scene):
    def construct_randpoints(self):
        points = []
        x = 4
        y = 3
        self.wait(1)
        for i in range(20):
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

    # Devuelve indices de los puntos que pertenecen a la izqueirda y derecha de la linea
    # formada por p1 y p2
    def div_sides(self, p1, p2, points):
        left = []
        right = []
        for i in range(len(points)):
            p = points[i].get_center()
            side = which_side(p1.get_center(), p2.get_center(), p)
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
    

class Animation(Basic_Animations):
    def construct(self):
        # In this function you do all the functions used for the final animation
        points = self.construct_randpoints()
        p_order = self.order_points(points)

        p1 = points[p_order[0]]
        p2 = points[p_order[-1]]

        convex_h1 = []
        convex_h1.append(p1)
        convex_h1.append(p2)

        convex_h2 = []


        self.join_points(p1, p2)
        l, r = self.div_sides(p1, p2, points)

        self.quickHull(points, p2, p1, l, convex_h1)
        self.quickHull(points, p1, p2, r, convex_h2)

        convex_h = convex_h2 + convex_h1

        for i in range(len(convex_h)-1):
            l = self.join_points(convex_h[i], convex_h[i+1])
            self.color_line(l, "RED")
        l = self.join_points(convex_h[-1], convex_h[0])
        self.color_line(l, "RED")

        self.wait(2)

    def quickHull(self, points, p1, p2, side, c_h):
        if len(side) == 0:
            return
        # Te devuelve el punto ma lejano del conjunto punto del lado side
        # ide contiene lo indices de points que estan en un lado
        p_l = self.lejano(p1, p2, points, side)
        pl = points[p_l]
        self.highlight_point(pl, "RED")
        self.join_points(p1, pl)
        self.join_points(pl, p2)

        # debe agregarse entre p_1 y p_2
        if len(c_h) < 2:
            c_h.append(pl)
        else:
            self.add_to_ch(c_h, p1, p2, pl)

        l, r = self.div_sides(p1, pl, points)
        self.quickHull(points, p1, pl, r, c_h)
        l, r = self.div_sides(pl, p2, points)
        self.quickHull(points, pl, p2, r, c_h)
        

if __name__ == "__main__":
    scene = Animation()
    scene.render()
