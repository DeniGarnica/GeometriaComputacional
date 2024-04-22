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
    def intersect_twolines_anim(self, x, y):
        # Agregamos el punto a la animacion en caso de que cruce
        dot1 = Dot(point=np.array([x, y, 0]))
        self.add(dot1)
        dot1.set_color("RED")
        self.wait(0.5)
