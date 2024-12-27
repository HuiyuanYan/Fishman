import pygame
from src.ui.game_scene import GameScene
from src.ui.level_selection import LevelSelection
from src.ui.message_box import MessageBox
from src.utils import *
from src.settings import Settings
from src.entites import Player
class MainMenu:
    def __init__(self, screen,background_image_path:str = 'fishman.png'):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.background_image_path = background_image_path
        self.load_image(f'{Settings.basic_settings.RESOURCE_PATH}/{background_image_path}')

        # 定义字体
        self.font = pygame.font.SysFont('simHei', 36)

        # 玩家生命值
        self.player_health = Settings.player_settings.health
        self.gold = Settings.player_settings.gold
        button_width = 200
        button_height = 50
        start_game_x = (self.screen_width - button_width) // 2
        start_game_y = (self.screen_height - button_height) // 2
        self.start_game_rect = pygame.Rect(start_game_x, start_game_y, button_width, button_height)
        self.start_game_text = self.font.render("开始游戏", True, StandardColor.WHITE)

        settings_x = (self.screen_width - button_width) // 2
        settings_y = start_game_y + button_height + 20  # 在开始游戏按钮下方间隔20像素
        self.settings_rect = pygame.Rect(settings_x, settings_y, button_width, button_height)
        self.settings_text = self.font.render("游戏设置", True, StandardColor.WHITE)


    def load_image(self,background_image_path):
        """根据给定的资源路径加载背景对应的图片。"""
        self.background_image = pygame.image.load(background_image_path)
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_game_rect.collidepoint(event.pos):
                    if self.player_health > 0:
                        print("开始游戏按钮被点击，生命值足够，进入关卡选择页面！")
                        level_selection = LevelSelection(self.screen,self.background_image_path)
                        selected_level = level_selection.run()
                        if selected_level:
                            scene_setting = Settings.get_scene_settings(selected_level)
                            game_scene = GameScene.from_screen_and_scene_setting(self.screen, scene_setting)
                            player = Player(
                                health=Settings.player_settings.health,
                                fishnet_num=Settings.player_settings.fishnet_num,
                                harpoon_num=Settings.player_settings.harpoon_num,
                                boat_params=Settings.player_settings.boat,
                                fishnet_params=Settings.player_settings.fishnet,
                                harpoon_params=Settings.player_settings.harpoon
                            )
                            game_scene.set_player(player)
                            result = game_scene.run()
                            if result == 0:
                                continue
                            if result == 1:
                                message = "闯关成功！得分：" + str(game_scene.player.score)
                            elif result == -1:
                                message = "闯关失败！得分：" + str(game_scene.player.score)
                            message_box = MessageBox(message)
                            message_box.show()
                    else:
                        print("生命值不足，无法开始游戏！")
                elif self.settings_rect.collidepoint(event.pos):
                    print("游戏设置按钮被点击")
                    return "settings"
        return True

    def draw(self):
        # 绘制背景
        self.screen.blit(self.background_image, (0, 0))

        # 绘制按钮
        pygame.draw.rect(self.screen, StandardColor.GREEN, self.start_game_rect)
        self.screen.blit(self.start_game_text, (self.start_game_rect.x + 25, self.start_game_rect.y + 10))
        pygame.draw.rect(self.screen, StandardColor.RED, self.settings_rect)
        self.screen.blit(self.settings_text, (self.settings_rect.x + 25, self.settings_rect.y + 10))

        # 绘制生命值文本
        health_text = self.font.render(f"生命值: {self.player_health}", True, StandardColor.RED)
        gold_text = self.font.render(f"金币: {self.gold}", True, StandardColor.RED)
        self.screen.blit(health_text, (10, 10))
        self.screen.blit(gold_text, (10, 50))

    def run(self):
        running = True
        while running:
            result = self.handle_events()
            if result is False:
                running = False
            elif result == "settings":
                # 这里后续可以添加打开游戏设置界面的逻辑，比如创建Settings类并调用其run方法等
                pass

            self.draw()
            pygame.display.flip()       