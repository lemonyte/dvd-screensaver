#----------------------------------------------------------------------#
# Customization Settings

# Ignore the config file and use these settings (for debugging)
ignore_config_file = False

# These settings only apply if ignore_config_file is set to True or the config file cannot be found
# Number of items bouncing around on screen
image_count = 1

# Style of image, can be either '1' or '2'
style = '1'

# Color type, can be 'preset', 'random', or 'constant'
color_type = 'preset'

# Transparency inversion, can be either 'normal' for 'inverted'
# If set to 'inverted' the colored areas of the image become clear and vice versa
transparency_inversion = 'normal'

# RGBA value for the image(s) if color_type is set to 'constant'
rgba = (255, 255, 255, 255)

# The maximum width and height of the image in pixels
image_size = (300, 300)

# RGB color of the background
background_color = (0, 0, 0)

# Refresh speed of the display loop in updates per second
# Larger value = faster speed
refresh_speed = 60

# Speed type, can be 'random' or 'constant'
speed_type = 'constant'

# If speed_type is set to 'constant' the integers are the x and y speed of the image in pixels
# If speed_type is set to 'random' the integers are the range for the speed to be chosen from
# '1' = 1x speed, '2' = 2x speed, '0.5' = 0.5x speed, etc
speed = [2, 2]

# Width and height of the screen in pixels
# Set to your displays resolution
display_width, display_height = 1920, 1080

# Path to the config file
config_file_path = r'%APPDATA%/LemonPi314/dvd-screensaver/config.json'
#----------------------------------------------------------------------#

import sys
import os
import time
import json
# Disable standard output so the pygame message doesnt show up
s = sys.stdout
sys.stdout = open(os.devnull, 'w')
import pygame
# Return standard output to normal
sys.stdout = s
from PIL import Image
from ctypes import windll
from random import choice, randrange, uniform
from config import menu

resource_dir = os.path.dirname(__file__)
config_file_path = os.path.expandvars(config_file_path)
args = [arg.lower() for arg in sys.argv]
if '/s' not in args and '-s' not in args and '/p' not in args and '-p' not in args:
    menu(config_file_path)
    sys.exit()


def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)


class ScreensaverImage:
    def __init__(self, screen: pygame.Surface, style: str, size: tuple[int, int], speed_type: str, speed: list[float, float], color_type: str, transparency_inversion: str, rgba: list[int, int, int, int]):
        self.screen = screen
        self.style = style
        self.size = size
        self.speed_type = speed_type
        self.speed = speed
        self.color_type = color_type
        self.transparency_inversion = transparency_inversion
        self.rgba = rgba

        if self.speed_type == 'random' and self.speed[0] != self.speed[1]:
            self.speed = [round(uniform(min(self.speed), max(self.speed)), 1), round(uniform(min(self.speed), max(self.speed)), 1)]
        else:
            self.speed = [self.speed[0], self.speed[1]]
        if randrange(0, 2) == 1:
            self.speed[0] = -self.speed[0]
        if randrange(0, 2) == 1:
            self.speed[1] = -self.speed[1]

        self.image_dir = resource_path(os.path.join('images', self.style, self.transparency_inversion))
        self.images = [Image.open(os.path.join(self.image_dir, file)) for file in os.listdir(self.image_dir)]
        for image in self.images:
            image.thumbnail(self.size)
        self.pick_image()
        self.constant_color = False
        self.pygame_image = pygame.image.fromstring(self.current_image.tobytes(), self.current_image.size, self.current_image.mode)
        self.rect = self.pygame_image.get_rect()
        self.rect.left = randrange(0, display_width - self.rect.width)
        self.rect.top = randrange(0, display_height - self.rect.height)
        self.change_color()

    def pick_image(self):
        self.current_image = choice(self.images[:-1])
        self.images.append(self.images.pop(self.images.index(self.current_image)))

    def change_color(self):
        if self.color_type == 'preset':
            self.pick_image()
        else:
            if self.color_type == 'constant':
                if self.constant_color:
                    return
                else:
                    self.constant_color = True
                    rgba = self.rgba
            else:
                rgba = (randrange(0, 256), randrange(0, 256), randrange(0, 256), 255)
            new_pixel_data = []
            image = self.current_image
            image.convert('RGBA')
            pixel_data = image.getdata()
            for item in pixel_data:
                if item[3] != 0:
                    new_pixel_data.append(rgba)
                else:
                    new_pixel_data.append(item)
            image.putdata(new_pixel_data)
            self.current_image = image
        image = self.current_image
        self.pygame_image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)

    def draw(self):
        self.screen.blit(self.pygame_image, self.rect)

    def move(self):
        self.rect.left += self.speed[0]
        self.rect.top += self.speed[1]
        if self.rect.left < 0 or self.rect.right > display_width:
            self.speed[0] = -self.speed[0]
            self.change_color()
        if self.rect.top < 0 or self.rect.bottom > display_height:
            self.speed[1] = -self.speed[1]
            self.change_color()


if not ignore_config_file:
    try:
        with open(config_file_path, 'r') as config_file:
            config = json.load(config_file)
        image_count = int(config['image_count'])
        style = str(config['style'])
        image_size = (int(config['image_size']['width']), int(config['image_size']['height']))
        color_type = str(config['color_type'])
        transparency_inversion = 'inverted' if bool(config['transparency_inversion']) else 'normal'
        rgba = (int(config['image_color']['r']), int(config['image_color']['g']), int(config['image_color']['b']), int(config['image_color']['a']))
        background_color = (int(config['background_color']['r']), int(config['background_color']['g']), int(config['background_color']['b']))
        refresh_speed = int(config['refresh_speed'])
        speed_type = str(config['image_speed']['type'])
        speed = [float(config['image_speed']['x']), float(config['image_speed']['y'])]
    except Exception:
        pass

pygame.init()
try:
    display_size = windll.user32.GetSystemMetrics(78), windll.user32.GetSystemMetrics(79)
except Exception:
    pass
display_width, display_height = display_size
image_size = (image_size[0] / 1920 * display_width, image_size[1] / 1080 * display_height)
speed = [speed[0] / refresh_speed * 60, speed[1] / refresh_speed * 60]
screen = pygame.display.set_mode(display_size, pygame.FULLSCREEN)
clock = pygame.time.Clock()
images = [ScreensaverImage(screen, style, image_size, speed_type, speed, color_type, transparency_inversion, rgba) for i in range(image_count)]
pygame.mouse.set_visible(False)
run = True
try:
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                break
        screen.fill(background_color)
        for image in images:
            image.move()
            image.draw()
        pygame.display.flip()
        time.sleep(1 / refresh_speed)
finally:
    pygame.mouse.set_visible(True)
    raise sys.exit()
