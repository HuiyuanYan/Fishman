import math
import pygame
from src.settings import Settings
class Harpoon:
    def __init__(
        self,
        name: str = "渔叉",
        speed: int = 5,
        attack: int = 5,
        size: tuple = (20, 20),
        image_path: str = 'harpoon.png'
    ):
        self.name = name
        self.speed = speed
        self.attack = attack
        self.size = size
        self.image_path = image_path
        self.x = 0
        self.y = 0
        # 起始位置
        self.start_position = (0, 0)
        # 目标位置
        self.target_x = 0
        self.target_y = 0
        # 标记鱼叉是否正在飞行
        self.is_flying = False
        self.load_image(f'{Settings.basic_settings.RESOURCE_PATH}/{self.image_path}')

    def load_image(self, image_path):
        """根据给定的资源路径加载鱼类对应的图片。"""
        if self.image_path:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, self.size)

    def fire(self, x0, y0, x1, y1):
        """
        发射鱼叉，设置起始位置和目标位置，并将其标记为正在飞行。
        """
        self.start_position = (x0, y0)
        self.target_x = x1
        self.target_y = y1
        self.x = x0
        self.y = y0
        self.is_flying = True
        # 根据起始位置和目标位置计算鱼叉的初始角度并旋转图片
        dx = x1 - x0
        dy = y1 - y0
        self.angle = math.atan2(dy, dx)
        self.image = pygame.transform.rotate(self.image, - math.degrees(self.angle))



    def move(self):
        """
        移动鱼叉的逻辑，根据当前位置和目标位置更新鱼叉的位置。
        """
        if not self.is_flying:
            return
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance <= self.speed:
            # 当鱼叉接近或到达目标位置时，停止飞行
            self.x = self.target_x
            self.y = self.target_y
            self.is_flying = False
        else:
            # 计算移动的比例
            move_ratio = self.speed / distance
            self.x += dx * move_ratio
            self.y += dy * move_ratio

    @property
    def is_moving(self):
        return self.is_flying

    def draw(self,screen):
        if self.is_moving:
            screen.blit(self.image,(self.x,self.y))