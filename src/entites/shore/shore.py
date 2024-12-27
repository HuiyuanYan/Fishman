# 指定utf-8编码格式
# -*- coding: utf-8 -*-
import pygame
from src.settings import Settings
class Shore:
    def __init__(
        self,
        size:tuple = (50,50),
        initial_position:tuple = (0,0),
        image_path:str = 'shore.png',
        fish_value:dict={
            'Shark': 10,
            'Tuna': 20,
            'Goldfish': 5,
        }
    ):
        self.x = initial_position[0]
        self.y = initial_position[1]
        self.size = size
        self.load_image(
            f'{Settings.basic_settings.RESOURCE_PATH}/{image_path}'
        )
        self.fish_value = fish_value
        pass

    def load_image(self,image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.size[0],self.size[1]))
    
    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))
    
    def trade(self,player):
        """
        交易玩家的渔获
        """
        for fish,num in player.catches.items():
            player.score += self.fish_value[fish] * num
        player.catches.clear()