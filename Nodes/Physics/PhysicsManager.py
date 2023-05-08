import Game, World
from Maths import Vector2
from CollisionUtil import CollisionUtil
from SAT import SAT
from Nodes.NodeBase import NodeBase
from Nodes.Physics.PolygonPhsxBody import PolygonPhsxBody
from RenderUtil import RenderUtil

class PhysicsManager(NodeBase):
    def __init__(self, world: World):
        super().__init__(world)

        self.game.screen_color = (0, 0, 0)

    def update(self, deltaTime: float):
        super().handle_events()
        self.phsx_nodes = self.get_physics_nodes()

        self.update_physics(deltaTime)

        for node in self.phsx_nodes:
            node.position = node.new_position 
            node.reconstruct_body()
    
    def update_physics(self, deltaTime: float):
        self.solve_collisions(deltaTime)
        self.calculate_velocity(deltaTime)
        self.calculate_new_node_positions(deltaTime)

    def get_physics_nodes(self):
        nodes = []
        for node in self.world.nodes:
            if isinstance(node, PolygonPhsxBody):
                nodes.append(node)
        return nodes

    # def calculate_acceleration(self):
    #     for node in self.phsx_nodes:
    #         #self.apply_force_to_acceleration(node)
    #         if node.apply_gravity:
    #             node.acceleration = node.impulse + Vector2(0, 9.8 * node.mass)

    def calculate_velocity(self, deltaTime: float):
        for node in self.phsx_nodes:
            node.velocity = node.velocity + node.impulse * deltaTime
            node.impulse = Vector2(0, 0)
            #node.acceleration = Vector2(0, 0)

            #node.velocity = node.velocity.truncate(1000)

    def calculate_new_node_positions(self, deltaTime: float):
        dampingFactor = 1.0 - 0.95
        frameDamping = pow(dampingFactor, deltaTime)

        for node in self.phsx_nodes:
            node.new_position = node.position + node.velocity * deltaTime
            node.velocity *= frameDamping

    # def apply_constraints(self):
    #     origin = Vector2(0, 0)
    #     radius = 200

    #     for node in self.phsx_nodes:
    #         # Get vector from origin to node.
    #         to_node = node.new_position - origin
    #         # Get the distance from the origin to the node.
    #         distance = to_node.length()

    #         if distance > radius - node.size:
    #             # Get the normalized vector from the origin to the node.
    #             to_node_norm = to_node / distance
    #             # Get the new position of the node.
    #             node.new_position = origin + to_node_norm * (radius - node.size)

    def solve_collisions(self, deltaTime: float):
         node_count = len(self.phsx_nodes)
         for i in range(node_count):
            for j in range(i + 1, node_count):
                node_a = self.phsx_nodes[i]
                node_b = self.phsx_nodes[j]

                if CollisionUtil.are_bounding_boxes_inside(node_a.bounds, node_b.bounds):
                    MTV_result = SAT.are_polygons_intersecting(node_a.world_vertices, node_b.world_vertices)
                    if MTV_result.overlapping:
                        axis_norm = MTV_result.overlaping_result.perp_axis.normalize()
                        length = MTV_result.overlaping_result.min_overlap
                        node_a.velocity = node_a.velocity - axis_norm * length


                        #contact_result = MTV_result.overlaping_result.contact_result




                        # if contact_result.move_away_axis.length() > 0:
                        #     axis_norm = contact_result.move_away_axis.normalize()
                        #     length = contact_result.move_away_axis.length()
                        #     node_a.velocity = axis_norm * -length
                        #     #node_b.velocity = axis * -length

                            # # Draw the contact
                            # contact_result: SAT.ContactResult = MTV_result.overlaping_result.contact_result
                            # self.world.draw_line(contact_result.vertex, contact_result.vertex + contact_result.move_away_axis, 4, RenderUtil.RED)
                            # self.world.draw_point(contact_result.vertex, 6, RenderUtil.RED)
                            # self.world.draw_point(contact_result.vertex + contact_result.move_away_axis, 6, RenderUtil.RED)
    
    # def calculate_new_node_position(self, node: PolygonPhsxBody, deltaTime: float):
    #     velocity = node.new_position - node.old_position
    #     # Save current position.
    #     node.old_position = node.new_position
    #     # Perform verlet integration.
    #     node.new_position = node.new_position + (velocity + node.acceleration * deltaTime * deltaTime)
    #     # Reset acceleration to 0.
    #     node.acceleration = Vector2(0, 0)

    # def apply_force_to_acceleration(self, node: PolygonPhsxBody):
    #     if node.mass == 0:
    #         node.acceleration = Vector2(0, 0)
    #         return
    #     node.acceleration = node.force / node.mass

