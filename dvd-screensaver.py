"""
# Credit
# Example project from repl.it
# Author: Edwin Kofler (eankeen)
# Website: https://repl.it/talk/learn/A-Starter-Guide-to-Pygame/11741
# Images from Google Images and the example project
# License: MIT License https://choosealicense.com/licenses/mit/
"""
# Customization Settings

# Number of items bouncing around on screen.
numberOfImages = 1

# Style of image. Any number from 1 to 4 [3 and 4 are broken at the moment]
imageType = "1"

# Color type.
# The first value is the colors used. "preset" or "random"
# The second value is the color inversion. "normal" or "inverted"
# When set to "inverted" the colored areas become clear and vice versa.
colorType = ["preset", "normal"]

# The maximum width and height of the image
# Measured in pixels
imageSize = [300, 300]

# Color of the background. Standard RGB value.
backgroundColor = (0, 0, 0)

# Amount of delay after every loop cycle. Larger value = slower speed.
# Measured in seconds.
refreshSpeed = 1/500

# The speed multiplier of the image on "x" and "y".
# The first value is the speed type. "random" or "constant"
# When set to "random" the next two integers are the range for the speed to be chosen from.
# When set to "constant" the next two integers are the speed for "x" and "y".
# Can only be a whole integer greater than zero.
# "1" = 1x speed, "2" = 2x speed, "0.5" = 0.5x speed, etc.
# Measured in pixels.
speedType = ["constant", 1, 1]

# Width and height of the screen in pixels.
# Set to your displays resolution.
width, height = 1920, 1080
#----------------------------------------------------------------------#

import sys, os , time, random, ctypes, getopt, winreg

def disablePrint():
    sys.stdout = open(os.devnull, "w")

def enablePrint():
    sys.stdout = sys.__stdout__

disablePrint()
import pygame
enablePrint()
from PIL import Image
from pathlib import Path
from configmenu import *

if str(sys.argv).find("/c") != -1:
    ConfigMenu()

pygame.init()

def ResourcePath(relativePath):
    try:
        basePath = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(basePath, relativePath)

workingDir = Path(ResourcePath("dvd-screensaver.py")).parent
projectDir = Path(os.getcwd())

user32 = ctypes.windll.user32
displaySize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)

width = displaySize[0]
height = displaySize[1]

imageSize[0] = imageSize[0]/1920*displaySize[0]
imageSize[1] = imageSize[1]/1080*displaySize[1]

class logo:
    def __init__(self):
        global imageType

        if speedType[0] == "random":
            self.imageSpeed = [random.randrange(speedType[1], speedType[2]) / 1.0, random.randrange(speedType[1], speedType[2]) / 1.0]

            if random.randrange(0, 2) == 1:
                self.imageSpeed[0] = -self.imageSpeed[0]

            if random.randrange(0, 2) == 1:
                self.imageSpeed[1] = -self.imageSpeed[1]

        elif speedType[0] == "constant":
            self.imageSpeed = [speedType[1] / 1.0, speedType[2] / 1.0]

        if workingDir.name.startswith("dvd"):
            self.imageDir = os.path.join(workingDir, "images", "")

        else:
            self.imageDir = os.path.join(workingDir, "dvd-screensaver", "images", "")
            
        imageType = os.path.join(imageType, "")
        colorType[1] = os.path.join(colorType[1], "")
        self.imageDirCurrent = os.path.join(self.imageDir, "current-image", "current-image.png")
        self.imageFiles = os.listdir(self.imageDir + imageType + colorType[1]) 
        self.PickImage()
        self.imageRect = self.imageDisplayed.get_rect()
        self.x = random.randrange(0, width-self.imageRect.width)
        self.y = random.randrange(0, height-self.imageRect.height)
        self.ChangeColor(colorType, imageType)

    def PickImage(self):
        randomFile = self.imageFiles[random.randrange(0, len(self.imageFiles)-1)]
        image = Image.open(self.imageDir + imageType + colorType[1] + randomFile)
        self.imageFiles.insert(len(self.imageFiles), self.imageFiles.pop(self.imageFiles.index(randomFile)))
        image.thumbnail(imageSize)
        image.save(self.imageDirCurrent)
        self.imageDisplayed = pygame.image.load(self.imageDirCurrent)

    def ChangeColor(self, colorType, imageType):
        if colorType[0] == "random":
            newPixelData = []
            image = Image.open(self.imageDirCurrent)
            image.convert("RGBA")
            pixelData = image.getdata()
            nextColor = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255), 255)

            for item in pixelData:
                if item[3] != 0:
                    newPixelData.append(nextColor)
                else:
                    newPixelData.append(item)

            image.putdata(newPixelData)
            image.save(self.imageDirCurrent)
            self.imageDisplayed = pygame.image.load(self.imageDirCurrent)

        if colorType[0] == "preset":
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

clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode(displaySize)
logos = []

for item in range(0, numberOfImages):
    logos.append(logo())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            pygame.mouse.set_visible(True)
            sys.exit(0)

    screen.fill(backgroundColor)

    for item in logos:
        item.DrawImage(screen)
        item.MoveImage()

    pygame.display.flip()
    time.sleep(refreshSpeed)