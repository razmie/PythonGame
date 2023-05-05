from ScriptBase import ScriptBase
from World import World
from Maths import Vector2
from Nodes.UI.ButtonWidget import ButtonWidget

class FrontendScript(ScriptBase):
    button_count: int = 0

    def __init__(self, world: World):
        super().__init__(world)

        self.create_button("test1", "Polygon & Point Collision Test")
        self.create_button("test2", "Polygon & Polygon Collision Test")
        self.create_button("test3", "Verlet Physics Test")
        self.create_button("test4", "Physics Test")

    def on_button_click(self, button: ButtonWidget):
        if button.name == "test1":
            self.game.load_level("Assets/Levels/Worlds/PolyPointCollisionTest/PolyPointCollisionTest.json")
        elif button.name == "test2":
            self.game.load_level("Assets/Levels/Worlds/PolyPolyCollisionTest/PolyPolyCollisionTest.json")
        elif button.name == "test3":
            self.game.load_level("Assets/Levels/Worlds/VerletTest/VerletTest.json")
        elif button.name == "test4":
            self.game.load_level("Assets/Levels/Worlds/PhysicsTest/PhysicsTest.json")

    def create_button(self, button_name: str, text: str):
        screen_size = self.world.game.screen.get_size()

        button_height = 24

        self.widget = ButtonWidget(self.world, button_name, self.on_button_click)
        self.widget.set(Vector2(0, self.button_count * button_height), Vector2(screen_size[0], button_height), (255, 255, 255), "font1_20", text, (255, 255, 255))
        self.widget.draw_border = True
        self.widget.border_color = (127, 127, 127)
        self.world.nodes.append(self.widget)
        self.button_count += 1