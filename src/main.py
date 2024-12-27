import sys,os
sys.path.append(os.getcwd())
import pygame
from src.ui import MainMenu
from src.settings import Settings
if __name__ == "__main__":
    pygame.init()
    screen_size = (
        Settings.basic_settings.window_width,
        Settings.basic_settings.window_height
    )
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption(f"{Settings.basic_settings.name}_{Settings.basic_settings.version}")

    background_image_path = Settings.basic_settings.background_image_path
    main_menu = MainMenu(screen,background_image_path)
    main_menu.run()

    pygame.quit()