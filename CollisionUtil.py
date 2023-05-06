from math import sqrt
from Maths import Vector2, Rect

class CollisionUtil:
    # Checks if a point is inside a polygon.
    # This implementation uses the ray casting method to determine if a point is inside a polygon.
    # The idea is to cast a horizontal ray from the point to the right and count the number of 
    # intersections with the polygon. If the number of intersections is odd, the point is inside 
    # the polygon; if it's even, the point is outside the polygon.
    # https://www.youtube.com/watch?v=RSXM9bgqxJM
    @staticmethod
    def is_point_in_polygon(point: Vector2, vertices: list[Vector2]) -> bool:
        n = len(vertices)

        p1 = vertices[0]
        inside_count = 0

        for i in range(n + 1):
            p2 = vertices[i % n]
            if point.y > min(p1.y, p2.y):
                if point.y <= max(p1.y, p2.y):
                    if point.x <= max(p1.x, p2.x):
                        # Find x intersection betwen horizontal line starting from x and the polygon line.
                        xinters = (point.y - p1.y) / (p2.y - p1.y) * (p2.x - p1.x) + p1.x
                        if point.x <= xinters:
                            inside_count += 1
            p1 = p2

        return inside_count % 2 == 1 
    
    @staticmethod
    # Checks if boxes are intersecting using axis-aligned bounding boxes
    def are_bounding_boxes_inside(box1: Rect, box2: Rect):
        # if box1[1].x < box2[0].x or box1[0].x > box2[1].x:
        #     return False
        # if box1[1].y < box2[0].y or box1[0].y > box2[1].y:
        #     return False
        b1_right = box1.get_right()
        b1_bottom = box1.get_bottom()
        b2_right = box2.get_right()
        b2_bottom = box2.get_bottom()

        if b1_right < box2.position.x or box1.position.x > b2_right:
            return False
        if b1_bottom < box2.position.y or box1.position.y > b2_bottom:
            return False
        return True
    
    @staticmethod
    def project_polygon_onto_axis(vertices, axis: Vector2):
        # Project the polygon onto the axis.
        min = float('inf')
        max = float('-inf')
        for vertex in vertices:
            # Project the vertex onto the axis.
            projection = vertex.x * axis.x + vertex.y * axis.y
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
            edge = Vector2(p1.x - p2.x, p1.y - p2.y)
            # Get the perpendicular vector.
            axis = Vector2(-edge.y, edge.x)
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
