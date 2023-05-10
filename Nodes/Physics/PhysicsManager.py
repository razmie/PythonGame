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
        self.can_update = True
        self.phsx_update_per_frame = False

    def update(self, delta_time: float):
        super().handle_events()
        self.phsx_nodes = self.get_physics_nodes()

        # if self.can_update:

        #     if self.phsx_update_per_frame:
        #         self.can_update = False

        self.calculate_velocity(delta_time)
        self.calculate_new_node_positions(delta_time)
        self.solve_collisions(delta_time)

        for node in self.phsx_nodes:
            node.position = node.new_position 
            node.reconstruct_body()

            node.impulse = Vector2(0, 0)


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

    def calculate_velocity(self, delta_time: float):
        for node in self.phsx_nodes:
            if node.static == False:
                node.velocity = node.velocity + node.impulse
                #node.velocity = node.velocity.truncate(1000)

    def calculate_new_node_positions(self, delta_time: float):
        dampingFactor = 1.0 - 0.95
        #frameDamping = pow(dampingFactor, delta_time)

        for node in self.phsx_nodes:
            if node.static == False:
                node.new_position = node.position + node.velocity * delta_time
                #node.velocity *= frameDamping

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

    def solve_collisions(self, delta_time: float):
         node_count = len(self.phsx_nodes)
         for i in range(node_count):
            for j in range(i + 1, node_count):
                node_a = self.phsx_nodes[i]
                node_b = self.phsx_nodes[j]

                if CollisionUtil.are_bounding_boxes_inside(node_a.bounds, node_b.bounds):
                    MTV_result = SAT.are_polygons_intersecting(node_a.world_vertices, node_b.world_vertices)
                    if MTV_result.overlapping:
                        if node_a.static == False:
                            push_norm = MTV_result.overlaping_result1.push_direction
                            push = push_norm * MTV_result.overlaping_result1.overlap

                            reflection = node_a.velocity.reflect(MTV_result.overlaping_result1.push_direction)

                            prev_vel = node_a.velocity
                            vel_len = prev_vel.length()
                            if vel_len > 0:
                                opp_vel = (prev_vel.normalize() * -vel_len)
                            else:
                                opp_vel = Vector2(0, 0)
                            #node_a.velocity = (node_a.velocity + opp_vel)

                            #node_a.velocity += push * delta_time * node_a.mass
        
           
                            node_a.velocity += reflection
                            node_a.new_position += push
                            pass



 
    
    # def calculate_new_node_position(self, node: PolygonPhsxBody, delta_time: float):
    #     velocity = node.new_position - node.old_position
    #     # Save current position.
    #     node.old_position = node.new_position
    #     # Perform verlet integration.
    #     node.new_position = node.new_position + (velocity + node.acceleration * delta_time * delta_time)
    #     # Reset acceleration to 0.
    #     node.acceleration = Vector2(0, 0)

    # def apply_force_to_acceleration(self, node: PolygonPhsxBody):
    #     if node.mass == 0:
    #         node.acceleration = Vector2(0, 0)
    #         return
    #     node.acceleration = node.force / node.mass

