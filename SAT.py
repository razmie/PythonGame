from Maths import Vector2

class SAT:
    @staticmethod
    def project_polygon_onto_axis(vertices, axis: Vector2):
        # Project the polygon onto the axis.
        min = float('inf')
        max = float('-inf')
        min_vertex = Vector2()
        max_vertex = Vector2()
        for vertex in vertices:
            # Project the vertex onto the axis.
            projection = vertex.x * axis.x + vertex.y * axis.y
            # Update the min and max values.
            if projection < min:
                min = projection
                min_vertex = vertex        
            if projection > max:
                max = projection
                max_vertex = vertex
        # Return the min and max values.
        return min, max, min_vertex, max_vertex
    
    class OverlappingResult:
        def __init__(self):
            self.overlapping = False
            self.min_overlap = float('inf')
            self.test_vertex = Vector2()
            self.test_edge = Vector2()
            self.min_vertex1 = Vector2()
            self.min_vertex2 = Vector2()
            self.max_vertex1 = Vector2()
            self.max_vertex2 = Vector2()

    @staticmethod
    # Checks if polygon 1 is intersecting with polygon2 using the Separating Axis Theorem.
    def is_polygon_overlapping_with_polygon(vertices1, vertices2):
        result = SAT.OverlappingResult()
        
        # Check if there's a separating axis between the polygons.
        for i in range(len(vertices1)):
            # Get the current vertex and the next vertex.
            p1 = vertices1[i]
            p2 = vertices1[(i + 1) % len(vertices1)]
            # Subtract the two to get the edge vector.
            edge = Vector2(p2.x - p1.x, p2.y - p1.y)
            # Get the perpendicular vector.
            axis = Vector2(-edge.y, edge.x)
            # Project both polygons onto the axis.
            min1, max1, min_vert1, max_vert1 = SAT.project_polygon_onto_axis(vertices1, axis)
            min2, max2, min_vert2, max_vert2 = SAT.project_polygon_onto_axis(vertices2, axis)
            overlap = min(max1, max2) - max(min1, min2)
            # Check if the projections are overlapping.
            if overlap < 0:
                # There's a separating axis, so the polygons aren't intersecting.
                return result
            
            # Check if the overlap is the smallest so far.
            if overlap < result.min_overlap:
                result.min_overlap = overlap
                result.test_vertex = p1
                result.test_edge = edge
                result.min_vertex1 = min_vert1
                result.min_vertex2 = min_vert2
                result.max_vertex1 = max_vert1
                result.max_vertex2 = max_vert2
                # if max2 > max2:
                #     result.test_edge = result.test_edge * -1

        # There isn't a separating axis, so the polygons are intersecting.
        result.overlapping = True
        return result

    class Result:
        def __init__(self):
            self.overlapping = False
            self.min_overlap = Vector2()
            self.min_vertex = Vector2()
            self.max_vertex = Vector2()
            self.min_edge = Vector2()
            self.contact_point = Vector2()

    @staticmethod
    # Checks if two polygons are overlapping using the Separating Axis Theorem.
    def are_polygons_intersecting(vertices1, vertices2):
        result = SAT.Result()
        overlapping_result1 = SAT.is_polygon_overlapping_with_polygon(vertices1, vertices2)
        if overlapping_result1.overlapping:
            overlapping_result2 = SAT.is_polygon_overlapping_with_polygon(vertices2, vertices1)
            if overlapping_result2.overlapping:

                result.overlapping = True

                if overlapping_result1.min_overlap < overlapping_result2.min_overlap:
                    result.min_overlap = overlapping_result1.min_overlap
                    result.min_vertex = overlapping_result2.max_vertex1
                    result.max_vertex = overlapping_result1.min_vertex1
                    #result.min_edge = overlapping_result1.test_edge
                    #result.contact_point = overlapping_result1.min_vertex2
                else:
                    result.min_overlap = overlapping_result2.min_overlap
                    result.min_vertex = overlapping_result2.min_vertex1
                    result.max_vertex = overlapping_result1.min_vertex1
                    #result.min_edge = overlapping_result2.test_edge
                    #result.contact_point = overlapping_result2.min_vertex2
        return result