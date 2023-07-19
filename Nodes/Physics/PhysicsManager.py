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

        self.apply_gravity(delta_time)
        self.calculate_velocity(delta_time)
        self.calculate_new_node_positions(delta_time)
        self.solve_collisions(delta_time)

        for node in self.phsx_nodes:
            node.reconstruct_body()

    def apply_gravity(self, delta_time: float):
        down = Vector2(0,1)
        gravity = down * 9.81

        for node in self.phsx_nodes:
            if node.static == False:
                node.force += node.mass * gravity

    def get_physics_nodes(self):
        nodes = []
        for node in self.world.nodes:
            if isinstance(node, PolygonPhsxBody):
                nodes.append(node)
        return nodes

    def calculate_velocity(self, delta_time: float):
        for node in self.phsx_nodes:
            node.velocity += node.force/node.mass * delta_time

    def calculate_new_node_positions(self, delta_time: float):
        dampingFactor = 1.0 - 0.95
        #frameDamping = pow(dampingFactor, delta_time)

        for node in self.phsx_nodes:
            node.position += node.velocity * delta_time
            #node.velocity *= frameDamping
            node.force = Vector2(0, 0)

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
                            push = push_norm * MTV_result.overlaping_result1.depth

                            reflection = node_a.velocity.reflect(MTV_result.overlaping_result1.push_direction)

                            prev_vel = node_a.velocity
                            vel_len = prev_vel.length()
                            if vel_len > 0:
                                opp_vel = (prev_vel.normalize() * -vel_len)
                            else:
                                opp_vel = Vector2(0, 0)
                            #node_a.velocity = (node_a.velocity + opp_vel)

                            #node_a.velocity += push * delta_time * node_a.mass
        
           
                            #node_a.velocity += reflection
                            node_a.position += push


                            #node_a.velocity += push * delta_time
                            #ode_a.force += node_a.mass * push / delta_time
                            pass

