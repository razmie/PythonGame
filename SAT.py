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
            # True if the polygons are overlapping.
            self.overlapping = False
            # The smallest overlap found out of all tests.
            self.min_overlap = float('inf')

            self.min_vert1 = Vector2()
            self.min_vert2 = Vector2()

            self.nearest_vert = Vector2()

        def calculate_contact(self):
            proj = self.nearest_vert.project(self.min_vert1, self.min_vert2)

            # Get the vector from the start to the end.
            line = self.min_vert2 - self.min_vert1
            line_norm = line.normalize()
            # Get the vector from the start to the point.
            point = self.nearest_vert - self.min_vert1
            # Project the point onto the line.
            dot = point.dot(line.normalize())

            contact =  self.min_vert1 + line_norm * dot
            contact_axis = self.nearest_vert - contact

            capped = False
            line_length = line.length()
            if dot > line_length:
                dot = line_length
                capped = True
            elif dot < 0:
                dot = 0
                capped = True

            if capped:
                # The contact is between the line start and end.
                contact =  self.min_vert1 + line_norm * dot

            return contact, contact_axis

    @staticmethod
    # Checks if polygon 1 is intersecting with polygon2 using the Separating Axis Theorem.
    def is_polygon_overlapping_with_polygon(vertices1, vertices2):
        result = SAT.OverlappingResult()

        # Check if there's a separating axis between the polygons.
        for idx in range(len(vertices1)):
            # Get the current vertex and the next vertex.
            p1 = vertices1[idx]
            p2 = vertices1[(idx + 1) % len(vertices1)]
            # Subtract the two to get the edge vector.
            edge = Vector2(p2.x - p1.x, p2.y - p1.y)
            # Get the perpendicular vector.
            axis = Vector2(-edge.y, edge.x)
            # Project both polygons onto the axis.
            min1, max1, min_vert1, max_vert1 = SAT.project_polygon_onto_axis(vertices1, axis)
            min2, max2, min_vert2, max_vert2 = SAT.project_polygon_onto_axis(vertices2, axis)

            overlap_max = min(max1, max2)
            overlap_min = max(min1, min2)
            overlap = overlap_max - overlap_min

            # Check if the projections are overlapping.
            if overlap < 0:
                # There's a separating axis, so the polygons aren't intersecting.
                return result
            
            # Get the test vert value on the axis.
            projected_p1 = p1.x * axis.x + p1.y * axis.y
            
            # Check if the overlap is the smallest so far.
            if overlap < result.min_overlap:

                # It's possible to have multiple axes with the same overlap. We get the one where
                # the projected vert falls within the overlap.
                if projected_p1 >= overlap_min and projected_p1 <= overlap_max:
                    result.min_overlap = overlap
                    result.min_vert1 = p1
                    result.min_vert2 = p2

                    result.nearest_vert = max_vert2

        # There isn't a separating axis, so the polygons are intersecting.
        result.overlapping = True
        return result

    class Result:
        def __init__(self):
            self.overlapping = False
            self.min_overlap = Vector2()
            
            overlaping_result: SAT.OverlappingResult = None

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
                    result.overlaping_result = overlapping_result1
                else:
                    result.overlaping_result = overlapping_result2
        return result