# Entrar desde la terminal a la carpeta 
# python3 -m manim -pql Tutorial.py main Animation

from manim import *

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def border_points_x(points):
    max_x = points[0].x
    min_x = points[0].x

    for p in points:
        if p.x < min_x:
            min_x = p.x
        elif p.x > max_x:
            max_x = p.x
    return min_x, max_x
    
def vec_2points(p1, p2):
    return (p2.x - p1.x, p2.y - p1.y)

def cross_product(vec1, vec2):
    return vec1[0] * vec2[1] - vec1[1] * vec2[0]
    
def which_side(p1, p2, p3):
    vec1 = vec_2points(p1, p2)
    vec2 = vec_2points(p1, p3)
    cross_p = cross_product(vec1, vec2)
    if cross_p > 0:
        return 1 #Right
    elif cross_p < 0:
        return -1 #Left
    else: 
        return 0 #On the line


class Basic_Animations(Scene):
    def construct_randpoints(self):
        points = []
        x = 4
        y = 3
        self.wait(1)
        for i in range(20):
            points.append(Dot(point=np.array([np.random.uniform(-x, x), np.random.uniform(-y, y), 0])))
        group = VGroup(*points)
        self.play(Create(group, run_time=6.0))
        self.wait(1)
        return points

    def join_points(self, p1, p2):
        line = Line(p1, p2)
        self.play(Create(line, run_time=1.0))
        self.wait(2)
        return line

    def color_points(self, point, color):
        point.set_color(color)
        self.wait(2)
    
    def color_line(self, line, color):
        line.set_color(color)
        self.wait(2)

    def highlight_line(self, line, color):
        line.set_color(color)
        self.wait(2)
        line.set_color("WHITE")
        self.wait(1)
    
    def highlight_point(self, point, color):
        point.set_color(color)
        self.wait(2)
        point.set_color("WHITE")
        self.wait(1)


class Animation(Basic_Animations):
    def construct(self):
        # In this function you do all the functions used for the final animation
        p = self.construct_randpoints()
        l = self.join_points(p[0], p[1])
        self.highlight_line(l, "BLUE")
        self.color_points(p[2], "RED")

if __name__ == "__main__":
    scene = Animation()
    scene.render()
