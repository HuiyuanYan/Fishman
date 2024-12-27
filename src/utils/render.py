import pygame
import math
from PIL import Image, ImageSequence
import random
class ImageRender:
    def __init__(
        self,
        image_path,
        x,
        y,
        width,
        height
    ):
        # 加载图像资源
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))

    def render(self,screen):
        screen.blit(self.image, (self.x, self.y))

class GIFRender:
    def __init__(self,
        gif_path,
        x,
        y,
        width,
        height,
        FPS=30
    ):
        self.x = x
        self.y = y
        self.FPS = FPS
        self.frames = []
        self.frame_index = 0
        self.last_frame_time = 0
        self.frame_interval = 1000 // FPS  # 根据 FPS 计算帧间隔，单位为毫秒
        
        self.load_gif(gif_path)
        for i in range(len(self.frames)):
            self.frames[i] = pygame.transform.scale(self.frames[i], (width, height))
        

        self.now_frame = 0  # 当前帧的计数器
        self.all_frame = len(self.frames)  # 总帧数

    def load_gif(self,gif_path):
        # 使用 PIL 打开 GIF 文件
        with Image.open(gif_path) as gif:
            for frame in ImageSequence.Iterator(gif):
                # 将帧转换为 pygame 的 Surface 对象
                frame_image = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
                self.frames.append(frame_image)

        # 这里不知道为啥，解析的第一帧是空白帧率
        self.frames.pop(0)

    def render(self, screen):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_time >= self.frame_interval:
            self.last_frame_time = current_time
            # 使用 math.floor 向下取整达到降帧的效果
            self.now_frame = (self.now_frame + 1) % self.all_frame
            self.frame_index = math.floor(self.now_frame)
        frame = self.frames[self.frame_index]
        screen.blit(frame, (self.x, self.y))

class SolidColorRender:
    def __init__(self,
        x,
        y,
        width,
        height,
        color = None
    ):
        # 如果为none，则随机一种颜色
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        if color is None:
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        else:
            self.color = color

    def render(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))



class BackgroundRender:
    def __init__(self,
        render_type,
        x,
        y,
        width,
        height,
        **kwargs
    ):
        if render_type == "image":
            self.renderer = ImageRender(kwargs.get("image_path"),x,y,width,height)
        elif render_type == "gif":
            self.renderer = GIFRender(kwargs.get("gif_path"),x,y,width,height,FPS=20)
        elif render_type == "solid":
            self.renderer = SolidColorRender(kwargs.get("color",None))
        else:
            raise ValueError("Unsupported render type")

    def render(self, screen):
        self.renderer.render(screen)


# def main():
#     pygame.init()
#     screen = pygame.display.set_mode((800, 600))
#     # 第一个 BackgroundRender 用于纯色渲染
#     render1 = BackgroundRender("solid", color=(255, 0, 0))
#     # 第二个 BackgroundRender 用于图像渲染
#     render2 = BackgroundRender("image", image_path="resource/sky1.png")
#     # 第三个 BackgroundRender 用于 GIF 渲染
#     render3 = BackgroundRender("gif", gif_path="resource/sea.gif")

#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#         # 渲染纯色背景，占屏幕的上三分之一
#         render1.render(screen, 0, 0, 800, 200)
#         # 渲染图像背景，占屏幕的中三分之一
#         render2.render(screen, 0, 200, 800, 200)
#         # 渲染 GIF 背景，占屏幕的下三分之一
#         render3.render(screen, 0, 400, 800, 200)
#         # 刷新显示
#         pygame.display.flip()


# if __name__ == "__main__":
#     main()