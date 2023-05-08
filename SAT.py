from Maths import Vector2

class SAT:
    class ContactResult:
        def __init__(self):
            self.contact = Vector2()            
            self.axis = Vector2()
            self.axis_length = 0

            # If true, the contact vert was capped within the start and end of the axis.
            self.capped = False

    class OverlappingResult:
        def __init__(self):
            # True if the polygons are overlapping.
            self.overlapping = False
            # The smallest overlap found out of all tests.
            self.min_overlap = float('inf')

            self.min_vert1 = Vector2()
            self.min_vert2 = Vector2()

            self.nearest_vert = Vector2()

            self.contact_result = SAT.ContactResult()

        def calculate_contact(self):
            self.contact_result = SAT.ContactResult()

            # Get the vector from the start to the end.
            line = self.min_vert2 - self.min_vert1
            line_norm = line.normalize()
            # Get the vector from the start to the point.
            point = self.nearest_vert - self.min_vert1
            # Project the point onto the line.
            dot = point.dot(line.normalize())

            self.contact_result.contact =  self.min_vert1 + line_norm * dot
            self.contact_result.axis = self.nearest_vert - self.contact_result.contact

            line_length = line.length()
            if dot > line_length:
                dot = line_length
                self.contact_result.capped = True
            elif dot < 0:
                dot = 0
                self.contact_result.capped = True

            if self.contact_result.capped:
                # The contact is between the line start and end.
                self.contact_result.contact =  self.min_vert1 + line_norm * dot

            self.contact_result.axis_length = self.contact_result.axis.length()

    class MTVResult:
        def __init__(self):
            self.overlapping = False
            self.min_overlap = Vector2()
            
            #overlaping_result: SAT.OverlappingResult = None

    # Checks if two polygons are overlapping using the Separating Axis Theorem.
    @staticmethod
    def are_polygons_intersecting(vertices1, vertices2):
        result = SAT.MTVResult()
        overlapping_result1 = SAT.is_polygon_overlapping_with_polygon(vertices1, vertices2)
        if overlapping_result1.overlapping:
            overlapping_result2 = SAT.is_polygon_overlapping_with_polygon(vertices2, vertices1)
            if overlapping_result2.overlapping:

                result.overlapping = True

                # if overlapping_result1.min_overlap < overlapping_result2.min_overlap:
                #     result.overlaping_result = overlapping_result1
                # else:
                #     result.overlaping_result = overlapping_result2

                overlapping_result1.calculate_contact()
                overlapping_result2.calculate_contact()

                # Always use the contact that wasn't capped within the axis line.
                if overlapping_result1.contact_result.capped == False and overlapping_result2.contact_result.capped == True:
                    result.overlaping_result = overlapping_result1
                elif overlapping_result1.contact_result.capped == True and overlapping_result2.contact_result.capped == False:
                    result.overlaping_result = overlapping_result2
                else:
                    # If both weren't capped, use the one with the smallest axis length.
                    if overlapping_result1.contact_result.axis_length < overlapping_result2.contact_result.axis_length:
                        result.overlaping_result = overlapping_result1
                    else:
                        result.overlaping_result = overlapping_result2

        return result

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

    # Checks if polygon 1 is intersecting with polygon2 using the Separating Axis Theorem.
    @staticmethod
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