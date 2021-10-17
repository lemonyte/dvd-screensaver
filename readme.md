# DVD Screensaver
By [LemonPi314](https://github.com/LemonPi314)

Bouncing DVD logo screensaver for Windows.
## Credit
Example project by Edwin Kofler (eankeen) from https://repl.it/talk/learn/A-Starter-Guide-to-Pygame/  
Images from Google Images and the example project
## Requirements
- Windows operating system
- 15 MB of free space if you are using the `.exe` or `.scr` file
- 17 MB of free space for temporary files if you are using the `.exe` or `.scr` file
## Usage
### `.exe` File
Download the `dvd-screensaver.exe` file from the [latest release](https://github.com/LemonPi314/dvd-screensaver/releases/latest) and run it from any directory with this command: `./dvd-screensaver.exe -s`. The `.exe` file is only dependent on temporary files it creates which get deleted when the program exits.
### `.scr` File
Make sure you have administrator permissions on your PC.
Download the screensaver file `dvd-screensaver.scr` from the [latest release](https://github.com/LemonPi314/dvd-screensaver/releases/latest) and move it to `C:\Windows\System32`. Right click on it and select "Install". In the screensaver settings menu select "dvd-screensaver".
### `.py` File
#### Requirements
- [Python 3.9](https://www.python.org/downloads/) or higher
- [pygame](https://pypi.org/project/pygame/)
- [Pillow](https://pypi.org/project/Pillow/)
- [PySimpleGUI](https://pypi.org/project/PySimpleGUI/)
#### Executing
Download the source code from the [latest release](https://github.com/LemonPi314/dvd-screensaver/releases/latest) and unzip the downloaded file. Open a terminal window and navigate to the unzipped directory. Run this command to start the program: `python dvd-screensaver.py -s`. In order for the Python script to work the `images` directory must be in the same folder as the Python script. The directory structure should look like this.
```
dvd-screensaver
│   dvd-screensaver.py
│   config.py
│   
└───images
    │
    └───1
    │   │   ...
    │
    └───2
        │   ...
```
### Configuration
To open the configuration menu run the Python script, `.exe` file, or `.scr` file without the `-s` argument. The `-s` argument is required to run the screensaver without opening the configuration menu, see the [Microsoft Docs](https://docs.microsoft.com/en-us/troubleshoot/windows/win32/screen-saver-command-line) for more details. The configuration JSON file is saved in `%APPDATA%/LemonPi314/dvd-screensaver/config.json`.
#### Configuration Options
Option|Description
------|-----------
Number of images|Number of items bouncing around on screen
Image style|Style of image, can be either '1' or '2'
Refresh speed|Refresh speed of the display loop in updates per second. Values higher than 120 may cause it to not function properly
Image width, height|The maximum width and height of the image in pixels
Image speed type|Speed type, can be 'random' or 'constant'
Image speed x, y|If the speed type is set to 'constant' the integers are the x and y speed of the image in pixels. If the speed type is set to 'random' the integers are the range for the speed to be chosen from
Image color type|Color type, can be 'preset', 'random', or 'constant'
Image red, green, blue, alpha|RGBA value for the image(s) if the color type is set to 'constant'
Invert transparency|Transparency inversion, colored areas of the image become clear and vice versa
Background red, green, blue|RGB color of the background

## License
[MIT License](https://choosealicense.com/licenses/mit/)
