import math
import random
import pygame
from src.settings import Settings


class Fishnet:
    def __init__(
        self,
        name: str = "渔网",
        speed: int = 3,
        attack: int = 5,
        size: tuple = (50, 50),
        capacity: int = 3,
        image_path: str = 'fishnet.png'
    ):
        self.name = name
        self.speed = speed
        self.attack = attack
        self.size = size
        self.capacity = capacity
        self.image_path = image_path
        self.x = 0
        self.y = 0
        # 起始位置
        self.start_position = (0, 0)
        # 目标位置（发射阶段）
        self.target_x = 0
        self.target_y = 0
        # 标记渔网是否正在发射
        self.is_launching = False
        # 标记渔网是否正在回收
        self.is_retrieving = False
        # 存储捕捉到的鱼的列表
        self.caught_fish = []
        self.load_image(f'{Settings.basic_settings.RESOURCE_PATH}/{self.image_path}')

    def catch_fish(self,fish):
        if len(self.caught_fish) < self.capacity and not fish.is_caught:
            # 根据鱼的健康值和网的攻击力，随机一个概率捕捉鱼（鱼的健康值越少，网的攻击力越高，捕捉概率越大）
            capture_probability = fish.health / self.attack
            if random.random() < capture_probability:
                self.caught_fish.append(fish)
                fish.is_caught = True
                return True
        return False


    def load_image(self, image_path):
        """根据给定的资源路径加载渔网对应的图片。"""
        if self.image_path:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, self.size)

    def fire(self, x0, y0, x1, y1):
        """
        发射渔网，设置起始位置和目标位置，并将其标记为正在发射。
        """
        self.start_position = (x0, y0)
        self.target_x = x1
        self.target_y = y1
        self.x = x0
        self.y = y0
        self.is_launching = True
        self.is_retrieving = False
        # 根据起始位置和目标位置计算渔网的初始角度并旋转图片
        dx = x1 - x0
        dy = y1 - y0
        self.angle = math.atan2(dy, dx)
        self.image = pygame.transform.rotate(self.image, - math.degrees(self.angle))

    def move(self, boat_x, boat_y):
        """
        移动渔网的逻辑，根据当前位置和目标位置更新渔网的位置，包括发射和回收阶段。
        """

        if self.is_launching:
            # 计算从起始位置到目标位置的位移
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance <= self.speed:
                # 到达目标位置，开始回收
                self.is_launching = False
                self.is_retrieving = True
                # 当开始回收时，将目标位置更新为小船的位置
            else:
                # 计算移动的比例
                move_ratio = self.speed / distance
                self.x += dx * move_ratio
                self.y += dy * move_ratio
        elif self.is_retrieving:
            # 计算从当前位置到小船位置的位移
            self.target_x = boat_x
            self.target_y = boat_y
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance <= self.speed:
                # 回到小船位置，结束回收
                self.x = self.target_x
                self.y = self.target_y
                #self.is_retrieving = False
            else:
                # 计算移动的比例
                move_ratio = self.speed / distance
                self.x += dx * move_ratio
                self.y += dy * move_ratio

        for fish in self.caught_fish:
            fish.target_x = self.target_x
            fish.target_y = self.target_y
            fish.speed = self.speed


    @property
    def is_moving(self):
        return self.is_launching or self.is_retrieving

    def draw(self,screen):
        if self.is_moving:
            screen.blit(self.image, (self.x, self.y))