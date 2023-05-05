from Maths import Vector2

# Gilbert-Johnson-Keerthi Algorithm implementation 
# to detect intersection between two convex polygons
class GTK:
    # Returns True if polygon1 and polygon2 intersect
    @staticmethod
    def intersect(polygon1: list, polygon2: list) -> bool: 
        ORIGIN = Vector2(0, 0)

        # def subtract(vector1: list, vector2: list) -> list:
        #     x1, y1 = vector1.x, vector1.y
        #     x2, y2 = vector2.x, vector2.y
        #     return Vector2(x1-x2, y1-y2)

        def dot(vector1: list, vector2: list) -> list:
            x1, y1 = vector1.x, vector1.y
            x2, y2 = vector2.x, vector2.y
            return x1*x2 + y1*y2

        def centroid(polygon: list) -> list:
            x = [vertex.x for vertex in polygon]
            y = [vertex.y for vertex in polygon]
            return Vector2(sum(x)/len(polygon), sum(y)/len(polygon))

        def normalize(vector: list) -> list: 
            x, y = vector.x, vector.y
            magnitude = (x*x + y*y)**0.5
            return Vector2(x/magnitude, y/magnitude)

        # Finds the support point in the Minkowski Difference, 
        # by taking the difference between the furthest point 
        # in the given direction in polygon1 and the furthest 
        # point in the opposite direction on polygon2.
        def get_support_point(polygon1: list, polygon2: list, direction: list) -> list:
            
            def get_furthest_point(polygon: list, direction: list) -> list:
                furthest_point = polygon[0]
                max_dot = dot(furthest_point, direction)
                for i in range(1, len(polygon)):
                    current_point = polygon[i]
                    current_dot = dot(current_point, direction)
                    if current_dot > max_dot:
                        max_dot = current_dot
                        furthest_point = current_point
                return furthest_point

            fp_shape1 = get_furthest_point(polygon1, direction)
            fp_shape2 = get_furthest_point(polygon2, ORIGIN - direction)
            return fp_shape1 - fp_shape2

        # Depending on the size of the simplex, 
        # finds a new direction and updates the 
        # simplex. Returns True if the simplex 
        # contains the ORIGIN.
        def handle_simplex(simplex: list, direction: list) -> bool:
            
            # Returns the vector triple product 
            # vector1 X vector2 X vector1, where
            # X represents cross product.
            def triple_cross(vector1: list, vector2: list) -> list:
                
                x1, y1 = vector1.x, vector1.y
                x2, y2 = vector2.x, vector2.y
                return Vector2(y1*(y1*x2 - x1*y2), x1*(x1*y2 - y1*x2))

            # Point A is the most recently added 
            # point to the simplex by convention. 
            # Returns False since we only have a 
            # line and the ORIGIN is not contained 
            # within the simplex yet.
            def handle_line(simplex: list, direction: list) -> False:
                
                B, A = simplex[0], simplex[1]
                AB, AO = B - A, ORIGIN - A
                AB_perpendicular = triple_cross(AB, AO)
                direction.x, direction.y = AB_perpendicular.x, AB_perpendicular.y
                return False

            # If dot(AB_perpendicular, AC) < 0, ORIGIN is in Voronoi region AB,
            # remove point C from the simplex. Similarly, point B is redundant
            # if dot(AC_perpendicular, AB) < 0. If none of those conditions
            # is satisfied, ORIGIN is in triangle ABC, return True.
            def handle_tri(simplex: list, direction: list) -> bool:
                C, B, A = simplex[0], simplex[1], simplex[2]
                AB, AC, AO = B - A, C - A, ORIGIN - A
                AB_perpendicular = triple_cross(AB, AO)
                AC_perpendicular = triple_cross(AC, AO)
                if dot(AB_perpendicular, AC) < 0 and dot(AC_perpendicular, AB) >= 0:
                    simplex.remove(C) 
                    direction.x, direction.y = AB_perpendicular.x, AB_perpendicular.y
                    return False
                elif dot(AB_perpendicular, AC) >= 0 and dot(AC_perpendicular, AB) < 0:
                    simplex.remove(B) 
                    direction.x, direction.y = AC_perpendicular.x, AC_perpendicular.y
                    return False
                return True
            
            return handle_line(simplex, direction) if len(simplex) == 2 else handle_tri(simplex, direction)

        # Initial direction could have been chosen 
        # randomly. Find the first support point and 
        # add it to the simplex. The next direction 
        # must be towards the ORIGIN.
        direction = normalize(centroid(polygon2) - centroid(polygon1)) 
        simplex = [get_support_point(polygon1, polygon2, direction)] 
        direction = ORIGIN - simplex[0] 
        
        # Get new support points. If point A doesn't
        # pass the ORIGIN, polygons do not intersect, 
        # return False. Else, add point to simplex.
        while True: 

            A = get_support_point(polygon1, polygon2, direction) 
            if dot(A, direction) < 0: return False 
            simplex.append(A) 
            if handle_simplex(simplex, direction): return True