import pygame
from src.settings import Settings
from src.utils import *

class LevelSelection:
    def __init__(self, screen, background_image_path):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.load_image(f"{Settings.basic_settings.RESOURCE_PATH}/{background_image_path}")
        self.font = pygame.font.SysFont('simHei', 24)
        self.levels = [i + 1 for i in range(Settings.basic_settings.level_number)]  # 从 basic_settings 中获取关卡数量
        self.level_rects = []
        self.selected_level = None

        # 定义关卡选择块的尺寸和间距
        button_width = 100
        button_height = 50
        spacing_x = 20  # 水平间距
        spacing_y = 20  # 垂直间距
        max_buttons_per_row = 5  # 每行最多显示的按钮数量

        # 计算起始位置
        start_x = (self.screen_width - (button_width * min(len(self.levels), max_buttons_per_row) + spacing_x * (min(len(self.levels), max_buttons_per_row) - 1))) // 2
        start_y = (self.screen_height - ((len(self.levels) // max_buttons_per_row + (1 if len(self.levels) % max_buttons_per_row > 0 else 0)) * (button_height + spacing_y))) // 2

        for i, level in enumerate(self.levels):
            row = i // max_buttons_per_row
            col = i % max_buttons_per_row
            level_x = start_x + col * (button_width + spacing_x)
            level_y = start_y + row * (button_height + spacing_y)
            level_rect = pygame.Rect(level_x, level_y, button_width, button_height)
            self.level_rects.append(level_rect)

    def load_image(self,background_image_path):
        self.background_image = pygame.image.load(background_image_path)
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))

    def handle_events(self):
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(self.level_rects):
                    if rect.collidepoint(event.pos):
                        print(i)
                        self.selected_level = self.levels[i]
                        return False
        return True
    
    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        for i, level in enumerate(self.levels):
            color = StandardColor.GREY if i!= self.selected_level else StandardColor.BLUE
            pygame.draw.rect(self.screen, color, self.level_rects[i])
            level_text = self.font.render(f"关卡{level}", True, StandardColor.GREEN)
            x = self.level_rects[i].x + 25
            y = self.level_rects[i].y + 10
            self.screen.blit(level_text, (x, y))

    def run(self):
        running = True
        while running:
            self.draw()
            result = self.handle_events()
            if result is False:
                running = False
                return self.selected_level

            
            pygame.display.flip()