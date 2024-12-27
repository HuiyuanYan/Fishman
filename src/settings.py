# settings.py
import os,sys
import yaml
from pathlib import Path
FISHMAN_ROOT = Path(os.environ.get("FISHMAN_ROOT", ".")).resolve()
sys.path.append(os.getcwd())
from src.pydantic_settings_file import *
from pathlib import Path

class BasicSettings(BaseFileSettings):
    
    model_config = SettingsConfigDict(yaml_file=FISHMAN_ROOT / "cfg/basic_settings.yaml")
    
    version: str = str("0.0.1")
    name: str = str("Fishman")

    background_image_path: str = "fishman.png"

    level_number: int = 4

    window_x: int = 100
    window_y: int = 100
    window_width: int = 800
    window_height: int = 600

    @cached_property
    def LOG_PATH(self) -> Path:
        """日志存储路径"""
        p = self.DATA_PATH / "logs"
        return p

    @cached_property
    def DATA_PATH(self) -> Path:
        """用户数据根目录"""
        p = FISHMAN_ROOT / "data"
        return p
    
    @cached_property
    def RESOURCE_PATH(self) -> Path:
        """资源文件根目录"""
        p = FISHMAN_ROOT / "resource"
        return p


    def make_dirs(self):
        '''创建所有数据目录'''
        for p in [
            self.LOG_PATH,
            self.DATA_PATH,
            self.RESOURCE_PATH
        ]:
            p.mkdir(parents=True, exist_ok=True)

class PlayerSettings(BaseFileSettings):
    
    model_config = SettingsConfigDict(yaml_file=FISHMAN_ROOT / "cfg/player_settings.yaml")

    health: int = 5

    fishnet_num: int = 5

    harpoon_num: int = 5

    gold: int = 100

    boat: dict = {
        "name": "小船",
        "image_path": "boat.png",
        "speed": 5,
        "timeout": 5,
        "size": {
            "width": 50,
            "height": 50
        }
    }

    fishnet: dict = {
        "name": "鱼网",
        "speed": 5,
        "durablity": 5
    }

    harpoon: dict = {
        "name": "鱼钩",
        "image_path": "harpoon.png",
        "speed": 5,
        "durablity": 5,
        "size":{
            "width": 40,
            "height": 20
        }
    }
    

class SceneSettings:
    def __init__(
        self,
        yaml_file_path: str = "scene1_settings.yaml"
    ):
        with open(yaml_file_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        self.timeout = config.get('timeout', 120)
        self.target = config.get('target', 100)
        self.sky = config.get('sky', {"image_path": "sky.png", "weight": 1})
        self.sea = config.get('sea', {"image_path": "sea.png", "weight": 2})
        self.dead_fish = config.get('dead_fish', {"image_path": "dead_fish.png", "size": {"width": 50, "height": 50}})
        self.caught_fish = config.get('caught_fish', {"image_path": "caught_fish.png", "size": {"width": 50, "height": 50}})
        self.shore = config.get('shore', {"image_path": "shore.png", "size": {"width": 50, "height": 50}})
        self.fish_setting = config.get('fish_setting', 
            {
                "Shark":{
                    "num":3,
                    "name":"鲨鱼",
                    "image_path":"shark.png",
                    "speed":0.5,
                    "attack":8,
                    "health":10,
                    "value":10,
                    "size":{
                    "width":100,
                    "height":100
                    }
                },
                "Tuna":{
                    "num":3,
                    "name":"龙鱼",
                    "image_path":"tuna.png",
                    "speed":1,
                    "attack":3,
                    "health":5,
                    "value":20,
                    "size":{
                    "width":50,
                    "height":50
                    }
                },
                "Goldfish":{
                    "num":10,
                    "name":"金鱼",
                    "image_path":"goldfish.png",
                    "speed":0.2,
                    "attack":0,
                    "health":5,
                    "value":5,
                    "size":{
                    "width":25,
                    "height":25
                    }
                }
            }
        )


class SettingsContainer:
    FISHMAN_ROOT = FISHMAN_ROOT
    basic_settings: BasicSettings = settings_property(BasicSettings())
    player_settings: PlayerSettings = settings_property(PlayerSettings())
    scene_settings_list: list[SceneSettings] = []

    def createl_all_templates(self):
        self.basic_settings.create_template_file(write_file=True)
        self.player_settings.create_template_file(write_file=True)

    def set_auto_reload(self, flag: bool=True):
        self.basic_settings.auto_reload = flag
        self.player_settings.auto_reload = flag
    
    def __init__(self) -> None:
        self.basic_settings.make_dirs()
        # 加载关卡配置
        for i in range(0,self.basic_settings.level_number):
            scene_settings = SceneSettings(yaml_file_path=FISHMAN_ROOT / f"cfg/scene{i+1}_settings.yaml")
            self.scene_settings_list.append(scene_settings)

    # 获取指定关卡配置
    def get_scene_settings(self, level: int)->SceneSettings:
        return self.scene_settings_list[level-1]

Settings = SettingsContainer()

if __name__ == "__main__":
    print(Settings.fish_settings.tuna["value"])