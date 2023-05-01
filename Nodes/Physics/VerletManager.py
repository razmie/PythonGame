import numpy as np
import inspect
import World
from Nodes.NodeBase import NodeBase
from Nodes.Physics.PointPhyNode import PointPhyNode

class VerletManager(NodeBase):
    def __init__(self, world: World):
        super().__init__(world)

        self.phy_accum_time = 0.0
        # How often the physics should be updated, seperate to game physics.
        self.phy_delta_time = 1/15

    def update(self, deltaTime: float):
        super().update(deltaTime)

        self.phy_accum_time = self.phy_accum_time + deltaTime
        if self.phy_accum_time >= self.phy_delta_time:
            self.phy_accum_time -= self.phy_delta_time
            self.update_physics(self.phy_delta_time)

        self.smooth_node_positions(deltaTime)
    
    def update_physics(self,deltaTime: float):
        self.phy_nodes = self.get_physics_nodes()

        substeps = 2
        subdt = deltaTime / substeps
        for i in range(substeps):
            self.apply_gravity()
            self.apply_constraints()
            self.solve_collisions()
            self.update_nodes(subdt)

    def get_physics_nodes(self):
        phy_node = []
        for node in self.world.nodes:
            if isinstance(node, PointPhyNode):
                phy_node.append(node)

        return phy_node

    def apply_gravity(self):
        for node in self.phy_nodes:
            self.accelerate_node(node, np.array([0, 9.81]))         

    def update_nodes(self, deltaTime: float):
        for node in self.phy_nodes:
            self.calculate_new_node_position(node, deltaTime)

    def apply_constraints(self):
        origin = np.array([0, 0])
        radius = 200

        for node in self.phy_nodes:
            # Get vector from origin to node.
            to_node = node.new_position - origin
            # Get the distance from the origin to the node.
            distance = np.linalg.norm(to_node)

            if distance > radius - node.size:
                # Get the normalized vector from the origin to the node.
                to_node_norm = to_node / distance
                # Get the new position of the node.
                node.new_position = origin + to_node_norm * (radius - node.size)

    def solve_collisions(self):
        node_count = len(self.phy_nodes)
        for i in range(node_count):
            for j in range(i + 1, node_count):
                node_a = self.phy_nodes[i]
                node_b = self.phy_nodes[j]

                # Get vector from node a to node b.
                atob = node_b.new_position - node_a.new_position
                # Get the distance from node a to node b.
                distance = np.linalg.norm(atob)

                # If node a and node b are overlapping excatly, move node b a little bit.
                if distance == 0.0:
                    node_b.new_position = node_b.new_position + np.array([0.001, 0.001])
                    atob = node_b.new_position - node_a.new_position
                    distance = np.linalg.norm(atob)

                if distance < node_a.size + node_b.size:
                    # Get the normalized vector from node a to node b.
                    atob_norm = atob / distance
                    delta = (node_a.size + node_b.size - distance)
                    # Get the new position of node a.
                    node_a.new_position = node_a.new_position - atob_norm * delta * 0.5
                    # Get the new position of node b.
                    node_b.new_position = node_b.new_position + atob_norm * delta * 0.5

    def smooth_node_positions(self, deltaTime: float):
        for node in self.phy_nodes:
            node.position = node.position + (node.new_position - node.position) * deltaTime * 20
    
    def calculate_new_node_position(self, node: PointPhyNode, deltaTime: float):
        velocity = node.new_position - node.old_position
        # Save current position.
        node.old_position = node.new_position
        # Perform verlet integration.
        node.new_position = node.new_position + (velocity + node.acceleration * deltaTime * deltaTime)
        # Reset acceleration to 0.
        node.acceleration = np.array([0, 0])

    def accelerate_node(self, node: PointPhyNode, acceleration: np.ndarray):
        node.acceleration = node.acceleration + acceleration * node.mass

