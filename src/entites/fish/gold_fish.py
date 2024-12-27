from src.entites.fish.fish import Fish
class Goldfish(Fish):
    def __init__(
        self,
        name: str = "金鱼",
        speed: int = 5,
        attack: int = 0,
        health: int = 5,
        value: int = 5,
        size: tuple = (25,25),
        image_path: str = "goldfish.png"
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