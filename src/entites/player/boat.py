import pygame
from src.utils import *
from src.settings import Settings
class Boat:
    def __init__(
            self,
            name = "小船",
            speed:int = 1,
            size:tuple = (50,50),
            image_path = 'boat.png',
            initial_position:tuple = (400,200)
        ):
        self.name = name
        self.speed = speed
        self.size = size
        # 小船当前位置坐标（初始值示例，可根据游戏实际场景调整）
        self.x = initial_position[0]
        self.y = initial_position[1] - self.size[1]
        # 小船移动方向（用于控制连续移动时的方向，初始化为None）
        self.direction = None
        self.image_path = image_path
        self.load_image(f'{Settings.basic_settings.RESOURCE_PATH}/{self.image_path}')

    def load_image(self, image_path):
        """根据给定的资源路径加载小船对应的图片。"""
        if image_path:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, self.size)

    def update_direction(self, direction):
        """
        根据传入的方向更新小船的移动方向。
        """
        self.direction = direction

    def move(self):
        """
        根据当前的移动方向移动小船。
        """
        if self.direction == "left":
            self.x = self.x - self.speed
        elif self.direction == "right":
            self.x = self.x + self.speed
        
    def draw(self,screen):
        """
        在屏幕上绘制小船。
        """
        screen.blit(self.image, (self.x, self.y))