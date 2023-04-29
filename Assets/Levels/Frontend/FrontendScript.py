from WorldScript import ScriptBase
from World import World
from Nodes.UI.PanelWidget import PanelWidget

class FrontendScript(ScriptBase):
    def __init__(self, world: World):
        super().__init__(world)

        self.widget = PanelWidget(world, (400,400), (0, 0), (100, 100), (0,0,255))
        self.world.nodes.append(self.widget)

        self.widget2 = PanelWidget(world, (100,0), (0, 0), (200, 50), (0,255,0))
        self.widget2.parent_node = self.widget
        self.world.nodes.append(self.widget2)

        self.widget3 = PanelWidget(world, (200,0), (0, 0),(50, 100), (255,255,0))
        self.widget3.parent_node = self.widget2
        self.world.nodes.append(self.widget3)
