import math

class Vector2:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y
        
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector2(self.x / other, self.y / other)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def set(self, other):
        self.x = other.x
        self.y = other.y

    def set(self, lst: list):
        if len(lst) != 2:
            raise ValueError("Vector2 must be initialized with a list of two numbers")
        self.x = lst[0]
        self.y = lst[1]

    def dot(self, other):
        return self.x * other.x + self.y * other.y
    
    def cross(self, other):
        return self.x * other.y - self.y * other.x
    
    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx*dx + dy*dy)
    
    def length(self):
        return math.sqrt(self.x*self.x + self.y*self.y)

    def truncate(self, max_length):
        if self.length() > max_length:
            return self.normalize() * max_length
        return self
    
    def normalize(self):
        len = self.length()
        return Vector2(self.x / len, self.y / len)
    
    def perpendicular(self):
        return Vector2(-self.y, self.x)
    
    def project(self, start, end, within_line = False):
        # Get the vector from the start to the end.
        line = end - start
        line_norm = line.normalize()
        # Get the vector from the start to the point.
        point = self - start
        # Project the point onto the line.
        dot = point.dot(line.normalize())

        if within_line:
            line_length = line.length()
            if dot > line_length:
                dot = line_length
            elif dot < 0:
                dot = 0

        projection = line_norm * dot

        return start + projection
    
    def reflect(self, normal):
        dot_product = (self.x * normal.x + self.y * normal.y)
        reflected = Vector2(self.x - 2 * dot_product * normal.x, self.y - 2 * dot_product * normal.y)
        return reflected

class Rect:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.position = Vector2(x, y)
        self.size = Vector2(width, height)

    def set(self, position: Vector2 = Vector2(), size: Vector2 = Vector2()):
        self.position = position
        self.size = size

    def set(self, position: Vector2, size: Vector2):
        self.position = position
        self.size = size

    def set(self, position: list, size: list):
        self.position.set(position)
        self.size.set(size)

    def set(self, position: tuple, size: tuple):
        self.position.set(position)
        self.size.set(size)

    def get_left(self):
        return self.position.x
    
    def get_top(self):
        return self.position.y
    
    def get_right(self):
        return self.position.x + self.size.x
    
    def get_bottom(self):
        return self.position.y + self.size.y
    
    def get_left_top(self):
        return self.position
    
    def get_right_bottom(self):
        return self.position + self.size

class Matrix3x3:
    def __init__(self, rows = [[1,0,0], [0,1,0], [0,0,1]]):
        if len(rows) != 3 or any(len(row) != 3 for row in rows):
            raise ValueError("Matrix3x3 must be initialized with a 3x3 list of numbers")
        self.rows = rows
        
    def __str__(self):
        return "\n".join(" ".join(str(val) for val in row) for row in self.rows)
    
    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(
                self.rows[0][0] * other.x + self.rows[0][1] * other.y + self.rows[0][2],
                self.rows[1][0] * other.x + self.rows[1][1] * other.y + self.rows[1][2]
            )
        elif isinstance(other, Matrix3x3):
            return Matrix3x3([
                [sum(self.rows[i][k] * other.rows[k][j] for k in range(3)) for j in range(3)]
                for i in range(3)
            ])
        else:
            raise TypeError("Matrix3x3 can only be multiplied by a Vector2 or another Matrix3x3")
        
    def __matmul__(self, other):
        return self.__mul__(other)
    
    def inverse(self):
        det = (
            self.rows[0][0] * (self.rows[1][1] * self.rows[2][2] - self.rows[1][2] * self.rows[2][1])
            - self.rows[0][1] * (self.rows[1][0] * self.rows[2][2] - self.rows[1][2] * self.rows[2][0])
            + self.rows[0][2] * (self.rows[1][0] * self.rows[2][1] - self.rows[1][1] * self.rows[2][0])
        )
        if det == 0:
            raise ValueError("Matrix3x3 is not invertible")

        inv_det = 1 / det
        a = self.rows[1][1] * self.rows[2][2] - self.rows[1][2] * self.rows[2][1]
        b = self.rows[0][2] * self.rows[2][1] - self.rows[0][1] * self.rows[2][2]
        c = self.rows[0][1] * self.rows[1][2] - self.rows[0][2] * self.rows[1][1]
        d = self.rows[1][2] * self.rows[2][0] - self.rows[1][0] * self.rows[2][2]
        e = self.rows[0][0] * self.rows[2][2] - self.rows[0][2] * self.rows[2][0]
        f = self.rows[0][2] * self.rows[1][0] - self.rows[0][0] * self.rows[1][2]
        g = self.rows[1][0] * self.rows[2][1] - self.rows[1][1] * self.rows[2][0]
        h = self.rows[0][1] * self.rows[2][0] - self.rows[0][0] * self.rows[2][1]
        i = self.rows[0][0] * self.rows[1][1] - self.rows[0][1] * self.rows[1][0]

        return Matrix3x3([
            [a * inv_det, b * inv_det, c * inv_det],
            [d * inv_det, e * inv_det, f * inv_det],
            [g * inv_det, h * inv_det, i * inv_det]
        ])

class Maths:
    @staticmethod
    def clip(val, min_val, max_val):
        return min(max(val, min_val), max_val)
    
    # Converts a list of Vector2 in a list of floats.
    @staticmethod
    def get_vertices(vertices: list[Vector2]):
        vertex_values = []
        for vertex in vertices:
            vertex_values.append((vertex.x, vertex.y))
        return vertex_values
    
    @staticmethod
    def pi():
        return math.pi
    
    @staticmethod
    def pi2():
        return math.pi * 2
    
    @staticmethod
    def pi4():
        return math.pi * 4
    
    @staticmethod
    def pi_2():
        return math.pi / 2
    
    @staticmethod
    def pi_4():
        return math.pi / 4
