import sys, ctypes, winreg, tkinter

registryPath = r"SOFTWARE\LemonPi314\dvd-screensaver"

def WriteRegistry(name, value):
    winreg.CreateKey(winreg.HKEY_CURRENT_USER, registryPath)
    registryKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registryPath, 0, winreg.KEY_WRITE)
    winreg.SetValueEx(registryKey, name, 0, winreg.REG_SZ, value)
    winreg.CloseKey(registryKey)

def ConfigMenu():
    WriteRegistry("numberOfImages", str(1))
    WriteRegistry("imageType", str(1))
    WriteRegistry("colorType_0", str("preset"))
    WriteRegistry("colorType_1", str("normal"))
    WriteRegistry("imageSize_0", str(300))
    WriteRegistry("imageSize_1", str(300))
    WriteRegistry("backgroundColor_R", str(0))
    WriteRegistry("backgroundColor_G", str(0))
    WriteRegistry("backgroundColor_B", str(0))
    WriteRegistry("refreshSpeed", str(1/500))
    WriteRegistry("speedType_0", str("constant"))
    WriteRegistry("speedType_1", str(1))
    WriteRegistry("speedType_2", str(1))
    WriteRegistry("width", str(1920))
    WriteRegistry("height", str(1080))

    window = tkinter.Tk()
    label = tkinter.Label(text="DVD Screensaver Configuration Options")
    buttonOK = tkinter.Button(text="OK", width=2, height=1)
    buttonCancel = tkinter.Button(text="Cancel", width=2, height=1)
    entryNumberOfImages = tkinter.Entry()

    label.pack()
    buttonOK.pack()
    buttonCancel.pack()
    entryNumberOfImages.pack()

    window.mainloop()

    ctypes.windll.user32.MessageBoxW(None, "Now do it again.", "Done?", 0)
    sys.exit(0)