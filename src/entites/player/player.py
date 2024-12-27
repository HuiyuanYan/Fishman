import pygame
from src.entites.player.boat import Boat
from src.entites.player.fishnet import Fishnet
from src.entites.player.harpoon import Harpoon


class Player:
    def __init__(
            self,
            health: int,
            fishnet_num: int,
            harpoon_num: int,
            boat_params: dict,
            fishnet_params: dict,
            harpoon_params: dict
    ):
        # 玩家生命值
        self.health = health
        self.score = 0
        self.fishnet_num = fishnet_num
        self.harpoon_num = harpoon_num
        self.harpoon_params = harpoon_params
        self.fishnet_params = fishnet_params
        # 实例化玩家拥有的小船对象
        self.boat = Boat(
            name=boat_params.get("name", "小船"),
            speed=boat_params.get("speed", 1),
            size = (boat_params.get("size", (50, 50))['width'], boat_params.get("size", (50, 50))['height']),
            image_path=boat_params.get("image_path", 'boat.png'),
        )
        # 实例化玩家拥有的鱼叉对象列表
        self.harpoons = []
        self.fishnets = []

        # 捕获的渔获字典
        self.catches = {}

    def handle_keyboard_input(self, key):
        """
        根据键盘按键处理玩家操作，比如控制小船移动方向等。
        """
        if key == pygame.K_a:
            self.boat.update_direction("left")
        elif key == pygame.K_d:
            self.boat.update_direction("right")


    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            self.handle_keyboard_input(event.key)
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_a, pygame.K_d]:
                self.boat.update_direction(None)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.button == 1:  # 鼠标左键
                # 发射鱼叉到鼠标点击位置
                self.fire_harpoon(mouse_x, mouse_y)
            elif event.button == 3:  # 鼠标右键
                # 发射渔网到鼠标点击位置
                self.fire_fishnet(mouse_x, mouse_y)


    def fire_harpoon(self, target_x, target_y):
        """
        模拟发射鱼叉的操作，设置鱼叉的起始位置和目标位置。
        """
        if len(self.harpoons) >= self.harpoon_num:
            return  # 鱼叉数量已达到上限，无法发射新的鱼叉
        harpoon = Harpoon(
            name=self.harpoon_params["name"],
            speed=self.harpoon_params["speed"],
            attack=self.harpoon_params["attack"],
            size=(self.harpoon_params["size"]["width"], self.harpoon_params["size"]["height"]),
            image_path=self.harpoon_params["image_path"]
        )
        harpoon.start_position = (self.boat.x, self.boat.y)
        harpoon.target_x = target_x
        harpoon.target_y = target_y
        harpoon.fire(self.boat.x, self.boat.y, target_x, target_y)
        self.harpoons.append(harpoon)


    def fire_fishnet(self, target_x, target_y):
        """
        模拟发射渔网的操作，设置渔网的起始位置和目标位置。
        """
        if len(self.fishnets) >= self.fishnet_num:
            return  # 渔网数量已达到上限，无法发射新的渔网
        fishnet = Fishnet(
            name=self.fishnet_params["name"],
            speed=self.fishnet_params["speed"],
            attack=self.fishnet_params["attack"],
            size=(self.fishnet_params["size"]["width"], self.fishnet_params["size"]["height"]),
            image_path=self.fishnet_params["image_path"]
        )
        fishnet.fire(self.boat.x, self.boat.y, target_x, target_y)
        self.fishnets.append(fishnet)
    
    def draw(self,screen):
        self.boat.draw(screen)
        for harpoon in self.harpoons:
            harpoon.draw(screen)
        for fishnet in self.fishnets:
            fishnet.draw(screen)
    
    def set_position(self,x,y):
        self.boat.x = x
        self.boat.y = y - self.boat.size[1]