from cx_Freeze import setup, Executable

setup(name='dvdscreensaver',
      version='1.0',
      description='DVD Screensaver',
      executables = [Executable("dvd-screensaver/dvd-screensaver.py")])