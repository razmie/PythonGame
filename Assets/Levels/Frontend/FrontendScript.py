from ScriptBase import ScriptBase
from World import World
from Nodes.UI.ButtonWidget import ButtonWidget

class FrontendScript(ScriptBase):
    button_count: int = 0

    def __init__(self, world: World):
        super().__init__(world)

        self.create_button("test1", "Point & Polygon Collision Test")
        self.create_button("test2", "Test 2")

    def on_button_click(self, button: ButtonWidget):
        if button.name == "test1":
            self.game.load_level("Assets/Levels/Worlds/PolygonCollisionTest/PolygonCollisionTest.json")

    def create_button(self, button_name: str, text: str):
        screen_size = self.world.game.screen.get_size()

        button_height = 24

        self.widget = ButtonWidget(self.world, button_name, self.on_button_click)
        self.widget.set([0, self.button_count * button_height], [screen_size[0], button_height], (255, 255, 255), "font1_20", text, (255, 255, 255))
        self.widget.draw_border = True
        self.widget.border_color = (127, 127, 127)
        self.world.nodes.append(self.widget)
        self.button_count += 1