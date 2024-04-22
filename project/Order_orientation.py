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
        side = which_side(p1, p2, points[i])
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

# Dadas dos rectas, nos dice si estas se intersectan y en que punto
# points = conjunto de todos los puntos
# i, i + 1 forman a la recta 1
# j, j + 1 forman a la recta 2
def intersect_twolines(p1, p2, p3, p4):
    # Los 4 puntos que conforman a los dos segmentos de recta
    '''p1 = points[2*i]
    p2 = points[2*i + 1]
    p3 = points[2*j]
    p4 = points[2*j + 1]'''

    # Vemos de que lado estan los puntos respecto al otro segmento de recta
    # Si alguno es 0 significa que esta en la linea
    s1 = which_side(p1, p2, p3)
    if s1 == 0:
        return 1, p3
    s2 = which_side(p1, p2, p4)
    if s2 == 0:
        return 1, p4
    s3 = which_side(p3, p4, p1)
    if s3 == 0:
        return 1, p1
    s4 = which_side(p3, p4, p2)
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

    return 1, [x, y]