
class CollisionUtil:
    # Checks if a point is inside a polygon.
    # This implementation uses the ray casting method to determine if a point is inside a polygon.
    # The idea is to cast a horizontal ray from the point to the right and count the number of 
    # intersections with the polygon. If the number of intersections is odd, the point is inside 
    # the polygon; if it's even, the point is outside the polygon.
    # https://www.youtube.com/watch?v=RSXM9bgqxJM
    @staticmethod
    def is_point_in_polygon(point: tuple, polygon: list[tuple]) -> bool:
        x, y = point
        n = len(polygon)
        inside = False
        p1x, p1y = polygon[0]
        inside_count = 0

        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        # Find x intersection betwen horizontal line starting from x and the polygon line.
                        xinters = (y - p1y) / (p2y - p1y) * (p2x - p1x) + p1x
                        if x <= xinters:
                            inside_count += 1
            p1x, p1y = p2x, p2y

        return inside_count % 2 == 1 