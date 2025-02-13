# DVD Screensaver

Bouncing DVD logo screensaver in Rust.

**README is a work in progress.**

## Usage

### `.scr` File

Download the `dvd-screensaver.scr` file from the [latest release](https://github.com/lemonyte/dvd-screensaver/releases/latest) and optionally move it to a user folder like `%APPDATA%/lemonyte/dvd-screensaver`. Right click on it and select "Install". In the screensaver settings menu select "dvd-screensaver". Moving the file to the `System32` folder is known to cause issues with x86 builds.

### Configuration

To open the configuration menu run the Python script, `.exe` file, or `.scr` file without the `-s` argument. The `-s` argument is required to run the screensaver without opening the configuration menu, see the [Microsoft Docs](https://docs.microsoft.com/en-us/troubleshoot/windows/win32/screen-saver-command-line) for more details. The configuration JSON file is saved in `%APPDATA%/lemonyte/dvd-screensaver/config.json`.

## Building

WIP

## Known Issues

- PC won't enter sleep mode if the screensaver is running

## License

[MIT License](license.txt)
