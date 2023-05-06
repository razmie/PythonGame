import World
from Maths import Vector2
from Nodes.NodeBase import NodeBase
from Nodes.Physics.PolygonPhsxBody import PolygonPhsxBody

class PhysicsManager(NodeBase):
    def __init__(self, world: World):
        super().__init__(world)

        self.phy_accum_time = 0.0
        # How often the physics should be updated, seperate to game physics.
        self.phy_delta_time = 1/30

    def update(self, deltaTime: float):
        self.phsx_nodes = self.get_physics_nodes()

        self.phy_accum_time = self.phy_accum_time + deltaTime
        if self.phy_accum_time >= self.phy_delta_time:
            self.phy_accum_time -= self.phy_delta_time
            self.update_physics(self.phy_delta_time)

        self.smooth_node_positions(deltaTime)
    
    def update_physics(self, deltaTime: float):
        substeps = 2
        subdelta = deltaTime / substeps
        for i in range(substeps):
            self.calculate_acceleration()
            #self.apply_constraints()
            #self.solve_collisions()
            self.calculate_new_node_positions(subdelta)
            self.calculate_velocity(subdelta)

    def get_physics_nodes(self):
        nodes = []
        for node in self.world.nodes:
            if isinstance(node, PolygonPhsxBody):
                nodes.append(node)
        return nodes

    def calculate_acceleration(self):
        for node in self.phsx_nodes:
            self.apply_force_to_acceleration(node)
            if node.apply_gravity:
                node.acceleration = node.acceleration + Vector2(0, 9.8 * node.mass)

    def calculate_velocity(self, deltaTime: float):
        for node in self.phsx_nodes:
            node.velocity = node.velocity + node.acceleration * deltaTime
            node.acceleration = Vector2(0, 0)

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

    # def solve_collisions(self):
    #     node_count = len(self.phsx_nodes)
    #     for i in range(node_count):
    #         for j in range(i + 1, node_count):
    #             node_a = self.phsx_nodes[i]
    #             node_b = self.phsx_nodes[j]

    #             # Get vector from node a to node b.
    #             atob = node_b.new_position - node_a.new_position
    #             # Get the distance from node a to node b.
    #             distance = atob.length()

    #             # If node a and node b are overlapping excatly, move node b a tiny bit.
    #             if distance == 0.0:
    #                 node_b.new_position = node_b.new_position + Vector2(0.001, 0.001)
    #                 atob = node_b.new_position - node_a.new_position
    #                 distance = atob.length()

    #             if distance < node_a.size + node_b.size:
    #                 # Get the normalized vector from node a to node b.
    #                 atob_norm = atob / distance
    #                 delta = atob_norm * 0.5 * (node_a.size + node_b.size - distance)
    #                 # Get the new position of node a.
    #                 node_a.new_position = node_a.new_position - delta
    #                 # Get the new position of node b.
    #                 node_b.new_position = node_b.new_position + delta

    def calculate_new_node_positions(self, deltaTime: float):
        dampingFactor = 1.0 - 0.95
        frameDamping = pow(dampingFactor, deltaTime)

        for node in self.phsx_nodes:
            node.new_position = node.position + node.velocity * deltaTime
            node.velocity *= frameDamping

    def smooth_node_positions(self, deltaTime: float):
        for node in self.phsx_nodes:
            #node.position = node.position + (node.new_position - node.position) * deltaTime * 20
            node.position = node.new_position 
            node.reconstruct_body()
    
    # def calculate_new_node_position(self, node: PolygonPhsxBody, deltaTime: float):
    #     velocity = node.new_position - node.old_position
    #     # Save current position.
    #     node.old_position = node.new_position
    #     # Perform verlet integration.
    #     node.new_position = node.new_position + (velocity + node.acceleration * deltaTime * deltaTime)
    #     # Reset acceleration to 0.
    #     node.acceleration = Vector2(0, 0)

    def apply_force_to_acceleration(self, node: PolygonPhsxBody):
        if node.mass == 0:
            node.acceleration = Vector2(0, 0)
            return
        node.acceleration = node.force / node.mass

