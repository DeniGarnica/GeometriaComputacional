import numpy as np
import Order_orientation as Oo
from manim import *

class Basic_Animations(Scene):
    # Crea n puntos aleatorios y hace su animacion de aparecerlos en la pantalla
    def construct_randpoints(self, n = 20):
        np.random.seed(0)
        points = []
        x = 4
        y = 3
        self.wait(1)
        for i in range(n):
            x_r = np.random.uniform(-x, x)
            y_r = np.random.uniform(-y, y)
            points.append(Dot(point=np.array([x_r, y_r, 0])))
        group = VGroup(*points)
        self.play(Create(group, run_time=2.0))
        self.wait(1)
        return points
    
    # Une co una recta los puntos p1 y p2
    def join_points(self, p1, p2):
        line = Line(p1, p2)
        self.play(Create(line, run_time=1.0))
        self.wait(0.1)
        return line

    # Cambia de color el punto point al color = color
    def color_point(self, point, color):
        point.set_color(color)
        self.wait(0.5)
    
    #Cambia de color de la linea al color = color
    def color_line(self, line, color):
        line.set_color(color)
        self.wait(0.1)

    def color_line_from_points(self, p1, p2, color):
        line = self.join_points(p1, p2)
        line.set_color(color)
        self.wait(0.1)

    # Resalta una recta con el color = color
    def highlight_line(self, line, color):
        line.set_color(color)
        self.wait(2)
        line.set_color("WHITE")
        self.wait(1)
    
    # Resalta una punto con el color = color
    def highlight_point(self, point, color):
        point.set_color(color)
        self.wait(1)
        point.set_color("WHITE")
        self.wait(1)

    # Crea n segmentos de recta en posiciones aleatorias
    def random_lines(self, n = 10):
        points = self.construct_randpoints(2*n)
        segments = []
        i = 0
        for j in range(n):
            # Que el primer punto del segmento tenga mayor coordenada y
            if points[i].get_center()[1] < points[i+1].get_center()[1]:
                aux = points[i]
                points[i] = points[i+1]
                points[i+1] = aux
            segments.append(self.join_points(points[i], points[i+1]))
            i = i + 2
        return segments, points
    
    '''
    Este codigo esta diseñado de tal manera que:
    dado el conjunto de puntos "points",
    points[i], points[i+1] forman el segmento (i/2)-ésimo
    además siempre points[i].y >= points[i+1].y
    
    Si dos rectas comparten un punto, este se almacena dos veces
    hay que marcar el no procesarlo dos veces (esto aun no se hace)
    '''

    # Dadas dos rectas, nos dice si estas se intersectan y en que punto
    # points = conjunto de todos los puntos
    # i, i + 1 forman a la recta 1
    # j, j + 1 forman a la recta 2
    def intersect_twolines(self, points, i, j):
        # Los 4 puntos que conforman a los dos segmentos de recta
        p1 = points[2*i]
        p2 = points[2*i + 1]
        p3 = points[2*j]
        p4 = points[2*j + 1]

        # Vemos de que lado estan los puntos respecto al otro segmento de recta
        # Si alguno es 0 significa que esta en la linea
        s1 = Oo.which_side(p1, p2, p3)
        if s1 == 0:
            return 1, p3
        s2 = Oo.which_side(p1, p2, p4)
        if s2 == 0:
            return 1, p4
        s3 = Oo.which_side(p3, p4, p1)
        if s3 == 0:
            return 1, p1
        s4 = Oo.which_side(p3, p4, p2)
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
