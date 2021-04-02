# DVD Screensaver
By [LemonPi314](https://github.com/LemonPi314)
## Credit
Example project from https://repl.it/  
Author: Edwin Kofler (eankeen).  
Website: https://repl.it/talk/learn/A-Starter-Guide-to-Pygame/11741  
Images from Google Images and the example project.
## Requirements
* Windows operating system
* 25 MB of free space if you are using the `.exe` or `.scr` file
* 85 MB of free space for temporary files if you are using the `.exe` or `.scr` file
## Usage
### `.exe` File
Download the `dvd-screensaver.exe` file from the `dist` directory and run it from any directory of your choice.
The `.exe` file is only dependent on temporary files it creates which get deleted when the program exits.
You may safely delete all other files that you downloaded.
### `.scr` File
Make sure you have administrator permissions on your pc.
Download the screensaver file `dvd-screensaver.scr` from the `dist` directory and move it to `C:\Windows\System32`.
Right click on it and select "Install"  
In the screensaver settings menu select "dvd-screensaver".
### `.py` File
#### Requirements
* Python 3.9 or higher
* [pygame](https://pypi.org/project/pygame/) `pip install pygame`
* [Pillow](https://pypi.org/project/Pillow/) `pip install Pillow`
#### Executing
Locate the file `dvd-screensaver.py` and double click to run it in the Python interpreter.  
To run the Python script only the `dvd-screensaver` subdirectory is needed.  
In order for the Python script to work the `images` directory must be in the same folder as the Python script.  
The folder which contains the script must be named `dvd-screensaver`.
```
dvd-screensaver
│   dvd-screensaver.py
│   dvd-screensaver.pyproj
│   
└───images
    │
    └───1
    │   │   ...
    │
    └───2
    │   │   ...
    │
    └───current-image
        │   current-image.png
```
## License
[MIT License](https://choosealicense.com/licenses/mit/)
