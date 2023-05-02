import numpy as np
import inspect
import World
from Nodes.NodeBase import NodeBase
from Nodes.Physics.PointPhsxBody import PointPhsxBody
from Nodes.Physics.PolygonPhsxBody import PolygonPhsxBody

class PhysicsManager(NodeBase):
    def __init__(self, world: World):
        super().__init__(world)

        self.phsx_nodes = []
        self.poly_nodes = []

    def update(self, deltaTime: float):
        self.get_physics_nodes()

        self.apply_gravity()
        #self.apply_constraints()
        self.update_nodes(deltaTime)

    def get_physics_nodes(self):
        self.phsx_nodes = []
        self.poly_nodes = []

        for node in self.world.nodes:
            if isinstance(node, PolygonPhsxBody):
                self.poly_nodes.append(node)
                self.phsx_nodes.append(node)
    
    def apply_gravity(self):
        for node in self.phsx_nodes:
            if node.mass != np.inf:
                node.acceleration = node.acceleration + np.array([0, 9.81]) * node.mass

    # def apply_constraints(self):
    #     origin = np.array([0, 0])
    #     radius = 200

    #     for node in self.phsx_nodes:
    #         # Get vector from origin to node.
    #         to_node = node.new_position - origin
    #         # Get the distance from the origin to the node.
    #         distance = np.linalg.norm(to_node)

    #         if distance > radius - 100:
    #             # Get the normalized vector from the origin to the node.
    #             to_node_norm = to_node / distance
    #             # Get the new position of the node.
    #             node.new_position = origin + to_node_norm * (radius - 100)

    def update_nodes(self, deltaTime: float):
        for node in self.phsx_nodes:
            self.calculate_new_node_position(node, deltaTime)
            
            node.position = node.new_position
            node.reconstruct_body()

    def calculate_new_node_position(self, node, deltaTime: float):
        velocity = node.new_position - node.old_position
        node.old_position = node.new_position
        node.new_position = node.new_position + (velocity + node.acceleration * deltaTime * deltaTime)
        node.acceleration = np.array([0, 0])

