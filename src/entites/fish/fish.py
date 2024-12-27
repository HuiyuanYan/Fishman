import pygame
from copy import deepcopy
from abc import ABC, abstractmethod
import random
import math

from src.settings import Settings

class Fish(ABC):
    def __init__(
        self,
        name:str,
        speed:float,
        attack:float,
        health:float,
        value:float,
        size:tuple,
        image_path:str
    ):
        self.name = name
        self.speed = speed
        self.attack = attack
        self.health = health
        self.value = value
        self.size = size
        self.image_path = image_path
        self.load_image(f'{Settings.basic_settings.RESOURCE_PATH}/{self.image_path}')

        # 鱼类的初始位置坐标（示例，可根据游戏实际场景调整）
        self.x = 0
        self.y = 0
        
        # 目标点坐标，用于鱼类移动时的目标位置
        
        self.last_target_update_time = 0
        
        # 攻击持续时间（以秒为单位），用于判断攻击是否结束
        self.attack_duration = 1000  # 攻击持续时间（毫秒）
        self.attack_start_time = -1  # 记录攻击开始时间

        # 新增记录上次攻击时间，控制攻击间隔
        self.last_attack_time = -1  # 上次攻击的时间
        self.attack_interval = 5000  # 攻击之间的间隔时间（毫秒）
        # 新增用于控制图片闪烁效果

        self.image_state = 0

        # 存储上一次的 dx 正负情况
        self.previous_dx_sign = None

        # 是否被渔网捕捉到
        self.is_caught = False

    # 设置鱼儿游动的边界
    def set_bound(self, upper_x, bottom_x, upper_y, bottom_y):
        """设置鱼儿游动的边界"""
        self.upper_x = upper_x
        self.bottom_x = bottom_x
        self.upper_y = upper_y
        self.bottom_y = bottom_y

    def set_random_target(self):
        """设置指定范围内的随机坐标点"""
        self.target_x = random.randint(self.bottom_x, self.upper_x)
        self.target_y = random.randint(self.bottom_y, self.upper_y)
        self.last_target_update_time = pygame.time.get_ticks()

    def move_towards_target(self):

        """鱼类朝着目标点移动的逻辑。"""
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > 0:
            move_step = min(self.speed, distance)
            self.x += dx / distance * move_step
            self.y += dy / distance * move_step
            dx_sign = 1 if dx > 0 else -1
            if dx_sign!= self.previous_dx_sign:
                if dx > 0:
                    self.image = pygame.transform.flip(self.image, True, False)
                self.previous_dx_sign = dx_sign
            
    def is_attacking(self):
        """判断鱼类是否正在攻击。"""
        if self.attack_start_time < 0:
            return False
        current_time = pygame.time.get_ticks()
        return current_time - self.attack_start_time < self.attack_duration

    def move(self):
        """鱼类的移动逻辑，控制是否在攻击状态时停止移动。"""
        current_time = pygame.time.get_ticks()

        self.update_image_state()

        if self.is_attacking():
            if not self.is_caught:
                return

        # 每隔一段时间更新目标点
        time_elapsed = current_time - self.last_target_update_time
        if time_elapsed > random.randint(3, 10) * 1000 and not self.is_caught:
            self.set_random_target()

        # 鱼类朝着目标点移动的逻辑
        self.move_towards_target()

    def attack_target(self, target):
        """鱼类攻击目标的逻辑，只有在攻击间隔时间足够时才可以继续攻击。"""
        current_time = pygame.time.get_ticks()

        # 判断是否足够时间进行下一次攻击
        if current_time - self.attack_start_time >= self.attack_interval:
            if self.__class__ != target.__class__:  # 确保攻击的是不同类的对象
                target.health = max(0,target.health-random.randint(0,self.attack))
                # 记录攻击开始的时间
                self.attack_start_time = current_time

    def update_image_state(self):
        """根据攻击状态更改图片显示状态"""
        #print(f"{self.name} update image state, attkack state is {self.is_attacking()}")
        #print(f'{self.name} attack state: {self.is_attacking()} , image state is {self.image_state}')
        if self.is_attacking():
            if self.image_state == 0:
                self.image = self.red_image# 攻击时变红
                self.image_state = 1
        else:
            if self.image_state == 1:
                #self.image.fill((255, 255, 255), special_flags=pygame.BLEND_RGBA_MULT)  # 恢复原色
                self.image = self.original_image  # 恢复原色
                self.image_state = 0
        #print(f'After image state is {self.image_state}')
    
    def load_image(self, image_path):
        """根据给定的资源路径加载鱼类对应的图片。"""
        if self.image_path:
            self.original_image = pygame.image.load(image_path)
            self.original_image = pygame.transform.scale(self.original_image, self.size)
            self.image = self.original_image
            self.red_image = self.original_image.copy()  # 保存原始图片
            self.red_image.fill((255, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        else:
            self.image = pygame.Surface(self.size)
            self.image.fill((255, 255, 255))  # 默认白色

    @classmethod
    def from_dict(cls, fish_dict):
        """使用字典参数初始化鱼类对象的类方法。"""
        required_keys = ["name", "speed", "attack", "health", "value", "size"]
        for key in required_keys:
            if key not in fish_dict:
                raise ValueError(f"字典中缺少必要的键 {key}")

        instance = cls(
            fish_dict["name"],
            fish_dict["speed"],
            fish_dict["attack"],
            fish_dict["health"],
            fish_dict["value"],
            (fish_dict["size"]["width"], fish_dict["size"]["height"]),
            fish_dict["image_path"]
        )
        return instance

    def is_dead(self):
        """判断鱼类是否死亡。"""
        return self.health <= 0

    def draw(self,screen):
        """绘制鱼类的方法，根据当前位置和图片进行绘制。"""
        if not self.is_dead():
            screen.blit(self.image, (self.x, self.y))