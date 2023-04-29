from WorldScript import ScriptBase
from World import World
from Nodes.UI.ButtonWidget import ButtonWidget

class FrontendScript(ScriptBase):
    def __init__(self, world: World):
        super().__init__(world)

        self.widget = ButtonWidget(world, self.on_button_click)
        self.widget.set([400, 400], [100, 100], (0, 0, 255))
        self.world.nodes.append(self.widget)

        self.widget2 = ButtonWidget(world, self.on_button_click)
        self.widget2.set([100, 0], [100, 100], (0, 255, 0))
        self.widget2.parent_node = self.widget
        self.world.nodes.append(self.widget2)

    def on_button_click(self, button: ButtonWidget):
        print("button clicked")