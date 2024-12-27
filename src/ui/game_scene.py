import pygame
import random
from src.entites import (
    Player,
    Shore,
    Shark,
    Goldfish,
    Tuna
)
from src.utils import *
from settings import Settings
import math

class GameScene:
    def __init__(self,
        screen,
        sky_param:dict = {
            "image_path": "sky.png",
            "weight": 1,
        },
        sea_param:dict = {
            "image_path": "sea.png",
            "weight": 2,
        },
        shore_param:dict = {
            "image_path": "shore.png",
            "size": {"width": 50, "height": 50}
        },
        dead_fish_param:dict = {
            "image_path": "dead_fish.png",
            "size": {"width": 30, "height": 20}
        },
        caught_fish_param:dict = {
            "image_path": "caught_fish.png",
            "size": {"width": 20, "height": 20}
        },
        fish_setting:dict = {
            "Shark": 1,
            "Tuna": 2,
            "Goldfish": 3
        },
        timeout = 120,
        target = 100
    ):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.total_weight = sky_param['weight'] + sea_param['weight']
        self.sky_weight = sky_param['weight']
        self.sea_weight = sea_param['weight']

        sky_image_path = sky_param['image_path']
        sea_image_path = sea_param['image_path']

        if sky_image_path.endswith('.png'):
            self.sky_renderer = BackgroundRender(
                "image",
                0, 0, self.screen_width, self.screen_height * self.sky_weight // self.total_weight,
                image_path=f'{Settings.basic_settings.RESOURCE_PATH}/{sky_param["image_path"]}'
            )
        elif sky_image_path.endswith('.gif'):
            self.sky_renderer = BackgroundRender(
                "gif",
                0, 0, self.screen_width, self.screen_height * self.sky_weight // self.total_weight,
                gif_path=f'{Settings.basic_settings.RESOURCE_PATH}/{sky_param["image_path"]}'
            )
        elif sky_image_path is None:
            print("sky image path is None, use random color")
            self.sky_renderer = BackgroundRender(
                "solid",
                0, 0, self.screen_width, self.screen_height * self.sky_weight // self.total_weight,
            )
        else:
            raise Exception("sky image path is not png or gif")


        if sea_image_path.endswith('.png'):
            self.sea_renderer = BackgroundRender(
                "image",
                0, self.screen_height * self.sky_weight // self.total_weight, self.screen_width, self.screen_height * self.sea_weight // self.total_weight,
                image_path=f'{Settings.basic_settings.RESOURCE_PATH}/{sea_param["image_path"]}'
            )
        elif sea_image_path.endswith('.gif'):
            self.sea_renderer = BackgroundRender(
                "gif",
                0, self.screen_height * self.sky_weight // self.total_weight, self.screen_width, self.screen_height * self.sea_weight // self.total_weight,
                gif_path=f'{Settings.basic_settings.RESOURCE_PATH}/{sea_param["image_path"]}'
            )
        elif sea_image_path is None:
            print("sea image path is None, use random color")
            self.sea_renderer = BackgroundRender(
                "solid",
                0, self.screen_height * self.sky_weight // self.total_weight, self.screen_width, self.screen_height * self.sea_weight // self.total_weight
            )
        else:
            raise Exception("sea image path is not png or gif")

        self.load_image(
            dead_fish_image_path=f'{Settings.basic_settings.RESOURCE_PATH}/{dead_fish_param["image_path"]}',
            caught_fish_image_path=f'{Settings.basic_settings.RESOURCE_PATH}/{caught_fish_param["image_path"]}',
            dead_fish_size=(dead_fish_param['size']["width"], dead_fish_param['size']["height"]),
            caught_fish_size=(caught_fish_param['size']["width"], caught_fish_param['size']["height"])
        )

        self.fish_setting = fish_setting

        

        self.font = pygame.font.SysFont('simHei', 36)
        
        # 实例化玩家对象
        self.player = None

        fish_value = {}
        for _, param in self.fish_setting.items():
            fish_value[param['name']] = param['value']
        self.shore = Shore(
            image_path = shore_param['image_path'],
            initial_position=(
                self.screen_width // 10,
                self.screen_height * self.sky_weight // self.total_weight - shore_param['size']['height']
            ),
            size = (shore_param['size']['width'], shore_param['size']['height']),
            fish_value=fish_value
        )
        
        # 初始化鱼类
        self.init_fish_list()
        self.dead_fish = []
        self.timeout = timeout
        self.target = target

        self.start_time = None
        self.elapsed_time = None

    def set_player(self,player:Player):
        if self.player is None:
            self.player = player
            self.player.set_position(self.screen_width // 10, self.screen_height* self.sky_weight// self.total_weight)
        else:
            raise Exception("Player already exists!")

    def load_image(
        self,
        dead_fish_image_path:str,
        caught_fish_image_path:str,
        dead_fish_size:tuple = (30,20),
        caught_fish_size:tuple = (20,20)
    ):
        self.dead_fish_image = pygame.image.load(dead_fish_image_path)
        self.dead_fish_image = pygame.transform.scale(self.dead_fish_image, dead_fish_size)
        
        self.caught_fish_image = pygame.image.load(caught_fish_image_path)
        self.caught_fish_image = pygame.transform.scale(self.caught_fish_image,caught_fish_size)
        pass


    def init_fish_list(self):
        """
        初始化鱼类的方法，这里示例创建了10条鱼，可根据实际情况增加或减少。
        """
        self.fish_list = []

        for class_name, param in self.fish_setting.items():
            num = param['num']
            for _ in range(num):
                fish = eval(class_name).from_dict(param)
                self.fish_list.append(fish)
        
        for fish in self.fish_list:
            fish.x = random.randint(0, self.screen_width)
            fish.y = random.randint(self.screen_height, self.screen_height)
        
        # 设置鱼儿游动边界和初始目标（不超过水面）
        for fish in self.fish_list:
            fish.set_bound(self.screen_width,0,self.screen_height,self.screen_height * self.sky_weight//self.total_weight)
            fish.set_random_target()
        pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if self.is_collision(self.player.boat, self.shore):
                        print("已靠岸，触发相关逻辑！")
                        self.shore.trade(self.player)
                        # 这里可以添加具体靠岸后的逻辑，比如补充物资、修理船只等
                    else:
                        print("还未靠近岸边，无法靠岸！")
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左键
                        # 获取鼠标点击位置
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        # 如果点击区域不在水面下，不需要玩家处理
                        if not (mouse_y > self.screen_height * self.sky_weight//self.total_weight):
                            continue
            self.player.handle_event(event)
        return True

    def check_bound(self,obj):
        """
        """
        obj.x = max(0, min(obj.x, self.screen_width - obj.size[0]))
        obj.y = max(self.screen_height * self.sky_weight//self.total_weight - obj.size[1], min(obj.y, self.screen_height - obj.size[1]))
        return

    def update(self):
        """
        更新游戏中各种元素的状态，比如小船的位置、鱼类的位置和状态等。
        """
        self.player.harpoons = [harpoon for harpoon in self.player.harpoons if harpoon.is_moving]
        self.player.fishnets = [fishnet for fishnet in self.player.fishnets if fishnet.is_moving]

        # 更新玩家的鱼叉位置和状态
        for harpoon in self.player.harpoons:
            harpoon.move()
            self.handle_harpoon_fish_collision(harpoon)

        # 更新渔网的位置和状态
        for fishnet in self.player.fishnets:
            fishnet.move(self.player.boat.x, self.player.boat.y)
            self.handle_fishnet_fish_collision(fishnet)
            self.handle_fishnet_boat_collision(fishnet)
        self.handle_fish_collisions()
        self.check_dead_fish()
    
        if self.player.boat.direction:
            self.player.boat.move()
            self.check_bound(self.player.boat)

        # 更新鱼类的位置和处理攻击逻辑
        for fish in self.fish_list:
            fish.move()
            self.check_bound(fish)
    
    def handle_fish_collisions(self):
        """
        处理鱼类之间碰撞及攻击逻辑的方法，通过两两比较鱼类来检测碰撞并处理攻击情况。
        """
        num_fish = len(self.fish_list)
        for i in range(num_fish):
            for j in range(i + 1, num_fish):
                fish1 = self.fish_list[i]
                fish2 = self.fish_list[j]
                if self.is_collision(fish1, fish2):
                    fish1.attack_target(fish2)
                    fish2.attack_target(fish1)

    def handle_harpoon_fish_collision(self, harpoon):
        """
        处理鱼叉与鱼的碰撞逻辑
        """
        for fish in self.fish_list:
            if self.is_collision(harpoon, fish):
                fish.health =max(0, fish.health - random.randint(0,harpoon.attack))
                harpoon.is_flying = False
    
    def handle_fishnet_fish_collision(self, fishnet):
        """
        处理渔网与鱼的碰撞逻辑
        """
        for fish in self.fish_list:
            if self.is_collision(fishnet, fish):
                fishnet.catch_fish(fish)
    
    def handle_fishnet_boat_collision(self, fishnet):
        """
        处理渔网与船的碰撞逻辑
        """
        #print(fishnet.x,fishnet.y,self.player.boat.x,self.player.boat.y)
        if self.is_collision(fishnet, self.player.boat):
            fishnet.is_retrieving = False
            # 对于渔网中的每条鱼，添加到玩家渔获中，并且删除该鱼
            for fish in fishnet.caught_fish:
                if fish.is_dead():
                    continue # 死鱼不算
                if fish.name not in self.player.catches:
                    self.player.catches[fish.name] = 0
                self.player.catches[fish.name] += 1
                print(f"捕获一条{fish.name}")
                # 删除该鱼
                fish.health = -1 # 捕获
            pass


    def draw(self):
        # 使用 BackgroundRender 绘制天空
        self.sky_renderer.render(self.screen)
        # 使用 BackgroundRender 绘制海洋
        self.sea_renderer.render(self.screen)
        # 绘制玩家得分
        score_text = self.font.render(f"当前得分：{self.player.score}  目标得分：{self.target}",True,StandardColor.ORANGE)
        self.screen.blit(score_text, (10, 10))

        if self.elapsed_time:
            time_text = self.font.render(f"时长：{self.timeout - self.elapsed_time}s", True, StandardColor.ORANGE)
            self.screen.blit(time_text, (10, 90))
        # 绘制捕获渔获
        catches_text = self.font.render(f"渔获：{self.player.catches}",True,StandardColor.ORANGE)
        self.screen.blit(catches_text, (10, 50))

        # 绘制海岸
        self.shore.draw(self.screen)

        # 绘制玩家相关元素
        self.player.draw(self.screen)

        # 绘制死鱼
        self.draw_dead_fish()

        # 绘制活鱼
        for fish in self.fish_list:
            fish.draw(self.screen)

    def run(self):
        self.start_time = pygame.time.get_ticks()
        running = True
        while running:
            result = self.handle_events()
            if result is False:
                running = False

            self.update()
            self.draw()
            pygame.display.flip()

            current_time = pygame.time.get_ticks()
            self.elapsed_time = (current_time - self.start_time) // 1000
            if self.player.score >= self.target:
                return 1
            else:
                if self.elapsed_time >= self.timeout:
                    return -1
                # catched字典为空
                if len(self.fish_list) == 0 and len(self.player.catches.keys()) == 0:
                    return -1
        return 0

    
    def is_collision(self, obj1, obj2,interval:int=20):
        """
        简单判断两个游戏对象是否发生碰撞的方法，这里示例通过距离判断，
        可根据实际情况采用更精确的碰撞检测算法，比如矩形碰撞检测等。
        """
        distance = math.sqrt((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2)
        return distance < interval  # 假设距离小于20像素算碰撞，可根据实际调整阈值
    

    def check_dead_fish(self):
        """
        检查鱼是否死亡，如果死亡，添加到 dead_fish 列表并从 fish_list 移除。
        """
        current_time = pygame.time.get_ticks()
        i = 0
        while i < len(self.fish_list):
            fish = self.fish_list[i]
            if fish.is_dead():
                self.dead_fish.append((fish.x, fish.y, current_time, fish.health))
                self.fish_list.pop(i)
            else:
                i += 1


    def draw_dead_fish(self):
        """
        绘制死鱼，根据死亡时间判断是否超过一秒，超过则移除。
        """
        current_time = pygame.time.get_ticks()
        # 使用for循环和enumerate同时获取索引和值
        for i, (x, y, death_time, health) in enumerate(self.dead_fish):
            if current_time - death_time < 1000:  # 持续一秒（1000毫秒）
                if health == 0:
                    # 被杀死
                    self.screen.blit(self.dead_fish_image, (x, y))
                elif health < 0:
                    # 被捕获
                    self.screen.blit(self.caught_fish_image,(x, y))
            else:
                # 如果超过一秒，则从列表中移除
                self.dead_fish.pop(i)
                # 由于列表被修改，需要跳过下一个元素，以避免索引错误
                continue
    
    @classmethod
    def from_screen_and_scene_setting(
        cls,
        screen,
        setting
    ):
        """
        从场景设置中创建游戏场景的方法，根据传入的设置来初始化游戏场景。
        """
        return cls(
            screen = screen,
            sky_param = setting.sky,
            sea_param = setting.sea,
            shore_param = setting.shore,
            dead_fish_param = setting.dead_fish,
            caught_fish_param = setting.caught_fish,
            fish_setting = setting.fish_setting,
            timeout = setting.timeout,
            target = setting.target
        )