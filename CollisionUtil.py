from math import sqrt

class CollisionUtil:
    # Checks if a point is inside a polygon.
    # This implementation uses the ray casting method to determine if a point is inside a polygon.
    # The idea is to cast a horizontal ray from the point to the right and count the number of 
    # intersections with the polygon. If the number of intersections is odd, the point is inside 
    # the polygon; if it's even, the point is outside the polygon.
    # https://www.youtube.com/watch?v=RSXM9bgqxJM
    @staticmethod
    def is_point_in_polygon(point: tuple, vertices: list[tuple]) -> bool:
        x, y = point
        n = len(vertices)
        inside = False
        p1x, p1y = vertices[0]
        inside_count = 0

        for i in range(n + 1):
            p2x, p2y = vertices[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        # Find x intersection betwen horizontal line starting from x and the polygon line.
                        xinters = (y - p1y) / (p2y - p1y) * (p2x - p1x) + p1x
                        if x <= xinters:
                            inside_count += 1
            p1x, p1y = p2x, p2y

        return inside_count % 2 == 1 
    
    @staticmethod
    def are_bounding_boxes_inside(box1: tuple, box2: tuple):
        if box1[1][0] < box2[0][0] or box1[0][0] > box2[1][0]:
            return False
        if box1[1][1] < box2[0][1] or box1[0][1] > box2[1][1]:
            return False
        return True
    
    @staticmethod
    def project_polygon_onto_axis(vertices, axis):
        # Project the polygon onto the axis.
        min = float('inf')
        max = float('-inf')
        for vertex in vertices:
            # Project the vertex onto the axis.
            projection = vertex[0] * axis[0] + vertex[1] * axis[1]
            # Update the min and max values.
            if projection < min:
                min = projection
            if projection > max:
                max = projection
        # Return the min and max values.
        return (min, max)

    @staticmethod
    # Checks if polygon 1 is intersecting with polygon2 using the Separating Axis Theorem.
    def is_polygon_intersecting_with_polygon(vertices1, vertices2):
        # Check if there's a separating axis between the polygons.
        for i in range(len(vertices1)):
            # Get the current vertex and the next vertex.
            p1 = vertices1[i]
            p2 = vertices1[(i + 1) % len(vertices1)]
            # Subtract the two to get the edge vector.
            edge = (p1[0] - p2[0], p1[1] - p2[1])
            # Get the perpendicular vector.
            axis = (-edge[1], edge[0])
            # Project both polygons onto the axis.
            min1, max1 = CollisionUtil.project_polygon_onto_axis(vertices1, axis)
            min2, max2 = CollisionUtil.project_polygon_onto_axis(vertices2, axis)
            # Check if the projections are overlapping.
            if max1 < min2 or max2 < min1:
                # There's a separating axis, so the polygons aren't intersecting.
                return False
        # There isn't a separating axis, so the polygons are intersecting.
        return True

    @staticmethod
    # Checks if two polygons are overlapping using the Separating Axis Theorem.
    def are_polygons_intersecting(vertices1, vertices2):
        if CollisionUtil.is_polygon_intersecting_with_polygon(vertices2, vertices2) and \
            CollisionUtil.is_polygon_intersecting_with_polygon(vertices2, vertices1):
            return True
        return False
    
    @staticmethod
    def distance(a, b):
        return sqrt((a.x - b.x)^2 + (a.y - b.y)^2)

    @staticmethod
    def are_circles_overlapping(position1, radius1, position2, radius2):
        r = radius1 + radius2
        return r < CollisionUtil.distance(position1, position2)

    @staticmethod
    def are_circles_overlapping_optimized(position1, radius1, position2, radius2):
        r = radius1 + radius2
        r *= r
        return r < (position1[0] + position2[0])^2 + (position1[1] + position2[1])^2
