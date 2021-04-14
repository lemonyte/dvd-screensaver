"""
# Credit
# Example project from repl.it
# Author: Edwin Kofler (eankeen)
# Website: https://repl.it/talk/learn/A-Starter-Guide-to-Pygame/11741
# Images from Google Images and the example project
# License: MIT License https://choosealicense.com/licenses/mit/
"""
#----------------------------------------------------------------------#
# Customization Settings

# Number of items bouncing around on screen.
numberOfImages = 1

# Style of image. Any number from 1 to 4 [3 and 4 are broken at the moment]
imageType = '1'

# Color type.
# The first value is the colors used. 'preset' or 'random'
# The second value is the color inversion. 'normal' or 'inverted'
# When set to 'inverted' the colored areas become clear and vice versa.
colorType = ['preset', 'normal']

# The maximum width and height of the image
# Measured in pixels
imageSize = [300, 300]

# Color of the background. Standard RGB value.
backgroundColor = (0, 0, 0)

# Amount of delay after every loop cycle. Larger value = slower speed.
# Measured in seconds.
refreshSpeed = 1/500

# The speed multiplier of the image on 'x' and 'y'.
# The first value is the speed type. 'random' or 'constant'
# When set to 'random' the next two integers are the range for the speed to be chosen from.
# When set to 'constant' the next two integers are the speed for 'x' and 'y'.
# Can only be a whole integer greater than zero.
# '1' = 1x speed, '2' = 2x speed, '0.5' = 0.5x speed, etc.
# Measured in pixels.
speedType = ['constant', 1, 1]

# Width and height of the screen in pixels.
# Set to your displays resolution.
width, height = 1920, 1080
#----------------------------------------------------------------------#

import sys, os , time, json

def DisablePrint():
    sys.stdout = open(os.devnull, 'w')

def EnablePrint():
    sys.stdout = sys.__stdout__

DisablePrint()
import pygame
EnablePrint()
from PIL import Image
from pathlib import Path
from ctypes import windll
from random import randrange
from gui import Menu

def ResourcePath(relativePath):
    try:
        basePath = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

    except:
        basePath = os.path.abspath('.')

    return os.path.join(basePath, relativePath)
    
resourceDir = Path(ResourcePath('dvd-screensaver.py')).parent
workingDir = Path(os.getcwd())

if '/c' in sys.argv:
    Menu(os.path.join(resourceDir, 'config.json'))
    sys.exit(0)

class image:
    def __init__(self):
        global imageType
        if speedType[0] == 'random':
            self.imageSpeed = [randrange(speedType[1], speedType[2]) / 1.0, randrange(speedType[1], speedType[2]) / 1.0]
            if randrange(0, 2) == 1:
                self.imageSpeed[0] = -self.imageSpeed[0]

            if randrange(0, 2) == 1:
                self.imageSpeed[1] = -self.imageSpeed[1]

        elif speedType[0] == 'constant':
            self.imageSpeed = [speedType[1] / 1.0, speedType[2] / 1.0]

        #if resourceDir.name.startswith('dvd'):
        self.imageDir = os.path.join(resourceDir, 'images', '')

        #else:
        #    self.imageDir = os.path.join(resourceDir, 'dvd-screensaver', 'images', '')
            
        imageType = os.path.join(imageType, '')
        if colorType[1] == 'true' or colorType[1] == 'inverted':
            colorType[1] = 'inverted/'

        else:
            colorType[1] = 'normal/'

        self.imageDirCurrent = os.path.join(self.imageDir, 'current-image', 'current-image.png')
        self.imageFiles = os.listdir(self.imageDir + imageType + colorType[1]) 
        self.PickImage()
        self.imageRect = self.imageDisplayed.get_rect()
        self.x = randrange(0, width-self.imageRect.width)
        self.y = randrange(0, height-self.imageRect.height)
        if colorType[1] == 'constant':
            self.ChangeColor(colorType, imageType, rgba)

        else:
            self.ChangeColor('random', imageType)

    def PickImage(self):
        randomFile = self.imageFiles[randrange(0, len(self.imageFiles) - 1)]
        image = Image.open(self.imageDir + imageType + colorType[1] + randomFile)
        self.imageFiles.insert(len(self.imageFiles), self.imageFiles.pop(self.imageFiles.index(randomFile)))
        image.thumbnail(imageSize)
        image.save(self.imageDirCurrent)
        self.imageDisplayed = pygame.image.load(self.imageDirCurrent)

    def ChangeColor(self, colorType, imageType, rgba = [randrange(0, 255), randrange(0, 255), randrange(0, 255), 255]):
        if colorType[0] == 'random':
            newPixelData = []
            image = Image.open(self.imageDirCurrent)
            image.convert('RGBA')
            pixelData = image.getdata()
            nextColor = tuple(rgba)
            for item in pixelData:
                if item[3] != 0:
                    newPixelData.append(nextColor)
                else:
                    newPixelData.append(item)

            image.putdata(newPixelData)
            image.save(self.imageDirCurrent)
            self.imageDisplayed = pygame.image.load(self.imageDirCurrent)

        elif colorType[0] == 'preset':
            self.PickImage()

    def DrawImage(self, screen):
        screen.blit(self.imageDisplayed, self.imageRect)
        
    def MoveImage(self):
        self.x += self.imageSpeed[0]
        self.y += self.imageSpeed[1]
        self.imageRect.top = self.y
        self.imageRect.left = self.x
        if self.imageRect.left < 0 or self.imageRect.right > width:
            self.imageSpeed[0] = -self.imageSpeed[0]
            self.ChangeColor(colorType, imageType)

        if self.imageRect.top < 0 or self.imageRect.bottom > height:
            self.imageSpeed[1] = -self.imageSpeed[1]
            self.ChangeColor(colorType, imageType)

pygame.init()
try:
    config = json.load(open('config.json', 'r'))
    numberOfImages = int(config['number_of_images'])
    imageType = config['image_type']
    imageSize = [int(config['image_size']['width']), int(config['image_size']['height'])]
    colorType = [config['image_color']['type'], config['image_color']['invert']]
    rgba = [int(config['image_color']['r']), int(config['image_color']['g']), int(config['image_color']['b']), int(config['image_color']['a'])]
    backgroundColor = (int(config['background_color']['r']), int(config['background_color']['g']), int(config['background_color']['b']))
    refreshSpeed = 1 / int(config['refresh_speed'])
    speedType = [config['image_speed']['type'], int(config['image_speed']['x']), int(config['image_speed']['y'])]
    width, height = int(config['screen_size']['width']), int(config['screen_size']['height'])

except:
    pass

displaySize = windll.user32.GetSystemMetrics(78), windll.user32.GetSystemMetrics(79)
width = displaySize[0]
height = displaySize[1]
imageSize[0] = imageSize[0] / 1920 * displaySize[0]
imageSize[1] = imageSize[1] / 1080 * displaySize[1]
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode(displaySize)
images = []
for item in range(0, numberOfImages):
    images.append(image())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            pygame.mouse.set_visible(True)
            sys.exit(0)

    screen.fill(backgroundColor)
    for item in images:
        item.MoveImage()
        item.DrawImage(screen)

    pygame.display.flip()
    time.sleep(refreshSpeed)