from Maths import Vector2

# Implementation of the Separating Axis Theorem (SAT) for collision detection.
class SAT:
    # class ContactResult:
    #     def __init__(self):
    #         self.vertex = Vector2()            
    #         # The axis the polygon needs to move away from to stop intersecting.
    #         self.move_away_axis = Vector2()
    #         # The length the polygon needs to move away from the axis to stop intersecting.
    #         self.move_away_length = 0
    #         # If true, the contact vert was capped within the start and end of the axis.
    #         self.capped = False

    class OverlappingResult:
        def __init__(self):
            # True if the polygons are overlapping.
            self.overlapping = False
            # The smallest overlap depth found out of all tests.
            self.depth = float('inf')
            # Vertex 1 on the edge that created the overlap. Belongs to the polygon that's being tested.
            self.v1 = Vector2()
            # Vertex 2 on the edge that created the overlap. Belongs to the polygon that's being tested.
            self.v2 = Vector2()
            # The vertex on other polygon of the polygon that's being tested.
            self.other_vert = Vector2()
            self.push_direction = Vector2()

            #self.contact_result = SAT.ContactResult()

        # def calculate_contact(self):
        #     self.contact_result = SAT.ContactResult()

        #     # Get the line vector from the start to the end.
        #     line = self.min_v2 - self.min_v1
        #     line_norm = line.normalize()

        #     # Project the nearest vertex onto the line.
        #     line_to_nearest = self.other_vert - self.min_v1
        #     dot = line_to_nearest.dot(line.normalize())

        #     self.contact_result.vertex =  self.min_v1 + line_norm * dot
        #     self.contact_result.move_away_axis = self.contact_result.vertex - self.other_vert

        #     # Check if the vertex has gone out of the line.
        #     line_length = line.length()
        #     if dot > line_length:
        #         dot = line_length
        #         self.contact_result.capped = True
        #     elif dot < 0:
        #         dot = 0
        #         self.contact_result.capped = True

        #     if self.contact_result.capped:
        #         # The contact is between the line start and end.
        #         self.contact_result.vertex = self.min_v1 + line_norm * dot

        #     self.contact_result.move_away_length = self.contact_result.move_away_axis.length()

    class MTVResult:
        def __init__(self):
            self.overlapping = False
            self.min_overlap = Vector2()

            self.overlaping_result1 = SAT.OverlappingResult()
            self.overlaping_result2 = SAT.OverlappingResult()

    @staticmethod
    def are_polygons_intersecting(vertices1, vertices2):
        result = SAT.MTVResult()

        overlapping_result1 = SAT.is_polygon_overlapping_with_polygon(vertices1, vertices2)
        if overlapping_result1.overlapping:
            overlapping_result2 = SAT.is_polygon_overlapping_with_polygon(vertices2, vertices1)
            if overlapping_result2.overlapping:
                result.overlapping = True
                result.overlaping_result1 = overlapping_result1
                result.overlaping_result2 = overlapping_result2

        return result

    # Pojects all vertices in a polygon onto an axis and returns the min and max values.
    @staticmethod
    def project_polygon_onto_axis(vertices, axis: Vector2):
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

        return min, max, min_vertex, max_vertex

    @staticmethod
    def is_polygon_overlapping_with_polygon(vertices1, vertices2):
        result = SAT.OverlappingResult()

        for idx in range(len(vertices1)):
            # Get the current vertex and the next vertex.
            p1 = vertices1[idx]
            p2 = vertices1[(idx + 1) % len(vertices1)]

            # Subtract the two to get the edge vector.
            edge = Vector2(p2.x - p1.x, p2.y - p1.y)
            # Get the perpendicular vector.
            perp_axis = Vector2(-edge.y, edge.x).normalize()

            # Project both polygons onto the axis.
            min1, max1, min_vert1, max_vert1 = SAT.project_polygon_onto_axis(vertices1, perp_axis)
            min2, max2, min_vert2, max_vert2 = SAT.project_polygon_onto_axis(vertices2, perp_axis)

            overlap_max = min(max1, max2)
            overlap_min = max(min1, min2)
            overlap = overlap_max - overlap_min

            # Check if the projections are overlapping.
            if overlap < 0:
                # There's a separating axis, so the polygons aren't intersecting.
                return result
            
            # Get the test vert value on the perp axis.
            projected_p1 = p1.x * perp_axis.x + p1.y * perp_axis.y
            
            # Check if the overlap is the smallest so far.
            if overlap < result.depth:
                # It's possible to have multiple axes with the same overlap. This can happen when there are parallel edges.
                # We get the one where the projected test vert falls within the overlap.
                if projected_p1 >= overlap_min and projected_p1 <= overlap_max:
                    result.depth = overlap
                    result.v1 = p1
                    result.v2 = p2
                    result.push_direction = perp_axis

                    result.other_vert = max_vert2
                    

        # There isn't a separating axis, so the polygons are intersecting.
        result.overlapping = True
        return result