from src.entites.fish.fish import Fish
class Tuna(Fish):
    def __init__(
        self,
        name: str = "金枪鱼",
        speed: int = 10,
        attack: int = 3,
        health: int = 5,
        value: int = 20,
        size: tuple = (50,50),
        image_path: str = "tuna.png"
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