from src.entites.fish.fish import Fish
class Shark(Fish):
    def __init__(
            self,
            name: str = "鲨鱼",
            speed: int = 5,
            attack: int = 8,
            health: int = 10,
            value: int = 10,
            size: tuple = (100, 100),
            image_path: str = "shark.png"
        ):
        super().__init__(
            name,
            speed,
            attack,
            health,
            value,
            size,
            image_path
        )