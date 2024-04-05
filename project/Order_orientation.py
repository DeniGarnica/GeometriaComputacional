def order_x(p):
    return p[0], p[1]

def order_y(p):
    return p[1], p[0]

def vec_2points(p1, p2):
    return (p2[0] - p1[0], p2[1] - p1[1])

def cross_product(vec1, vec2):
    return vec1[0] * vec2[1] - vec1[1] * vec2[0]

# calcula la distancia del punto p a la recta formada por p1 y p2
def lineDist(p1, p2, p):
    return abs((p[1] - p1[1]) * (p2[0] - p1[0]) -
            (p2[1] - p1[1]) * (p[0] - p1[0]))

# Regresa un arreglo del order de los puntos, no los puntos ordenados 
def order_points_x(points):
    return sorted(range(len(points)), key=lambda i: order_x(points[i].get_center()))

def order_points_y(points):
    return sorted(range(len(points)), key=lambda i: order_y(points[i].get_center()), reverse=True)


# Ve de que lado esta el punto p, respecto a la recta formada por p1, p2
def which_side(p1, p2, p):
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
def div_sides(p1, p2, points):
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
def lejano(p1, p2, points, side):
    max_d = 0.0
    ind = -1
    for i in range(len(side)):
        l_d = lineDist(p1.get_center(), p2.get_center(), points[side[i]].get_center())
        if l_d > max_d:
            max_d = l_d
            ind = side[i]
    return ind

def subset(points, side):
    sub = []
    for i in range(len(side)):
        sub.append(points[side[i]])
    return sub

# Ordena por el eje y los segmentos
def order_segments(points):
    segments = []
    s = sorted(range(len(points)), key=lambda i: order_y(points[i].get_center()))

    return segments

# Nos dice si el punto en la posicion i es un upper o lower
def upper_point(i):
    if i % 2 == 0:
        return 1 # devolveremos 1 para upper
    else:
        return 0

# Nos dice en que segmento se encuentra
def which_segment(i):
    return int(i/2)